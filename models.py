from sqlalchemy import ForeignKey, Integer, String, Text, JSON, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    industry: Mapped[str | None]
    employee_count: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    attributes: Mapped[list["CompanyAttribute"]] = relationship("CompanyAttribute",
                                                                cascade="all, delete-orphan")
    linked_attribute_groups: Mapped[list["CompanyAttributeGroup"]] = relationship("CompanyAttributeGroup",
                                                                                  back_populates="company",
                                                                                  cascade="all, delete-orphan")

    def __str__(self):
        return f"<Company (id={self.id}, name={self.name})>"

    def all_attributes(self):
        attrs = []
        for attr in self.attributes:
            attrs.append(attr.dict())

        for group in self.linked_attribute_groups:
            for attr in group.group.attributes:
                attrs.append(attr.dict())

        return attrs


class CompanyAttribute(Base):
    __tablename__ = "company_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    key: Mapped[str]
    value: Mapped[str]

    def __str__(self):
        return f"<CompanyAttribute (id={self.id}, company={self.company_id}, key={self.key}, value={self.value})>"

    def dict(self):
        return {self.key: self.value}


class AttributeGroup(Base):
    __tablename__ = "attribute_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_type: Mapped[str]
    label: Mapped[str | None]

    attributes: Mapped[list["AttributeGroupValue"]] = relationship("AttributeGroupValue", back_populates="group",
                                                                   cascade="all, delete-orphan")

    def dict(self):
        s = dict(sorted({i.key: i.value for i in self.attributes}.items()))
        return s

    def matchKeys(self):
        return list(self.dict().keys())

class AttributeGroupValue(Base):
    __tablename__ = "attribute_group_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("attribute_groups.id", ondelete="CASCADE"))
    key: Mapped[str]
    value: Mapped[str]

    group: Mapped["AttributeGroup"] = relationship("AttributeGroup", back_populates="attributes")

    def dict(self):
        return {self.key: self.value}


class CompanyAttributeGroup(Base):
    __tablename__ = "company_attribute_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    group_id: Mapped[int] = mapped_column(ForeignKey("attribute_groups.id", ondelete="CASCADE"))

    company: Mapped["Company"] = relationship("Company", back_populates="linked_attribute_groups")
    group: Mapped["AttributeGroup"] = relationship("AttributeGroup")


class SecurityControl(Base):
    __tablename__ = "security_controls"

    id: Mapped[int] = mapped_column(primary_key=True)
    control_id: Mapped[str]
    title: Mapped[str]
    description: Mapped[str | None]
    category: Mapped[str | None]
    framework: Mapped[str | None]

    safeguards: Mapped[list["Safeguard"]] = relationship("Safeguard", back_populates="control",
                                                         cascade="all, delete-orphan")

    def __str__(self):
        return f"<SecurityControl (id={self.control_id}, framework={self.framework}, #safeguards={len(self.safeguards)})>"


class Safeguard(Base):
    __tablename__ = "safeguards"

    id: Mapped[int] = mapped_column(primary_key=True)
    safeguard_id: Mapped[str]
    control_id: Mapped[int] = mapped_column(ForeignKey("security_controls.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None]

    control: Mapped["SecurityControl"] = relationship("SecurityControl", back_populates="safeguards")

    def __str__(self):
        return f"<Safeguard (id={self.safeguard_id}, title={self.title})>"


class RecommendationTemplate(Base):
    __tablename__ = "recommendation_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    safeguard_id: Mapped[int] = mapped_column(ForeignKey("safeguards.id", ondelete="CASCADE"))
    title: Mapped[str]
    description_template: Mapped[str]
    parameters_required: Mapped[list[str]] = mapped_column(JSON)

    def __str__(self):
        return f"<RecommendationTemplate (id={self.id}, safeguard={self.safeguard_id}, #parameters={len(self.parameters_required)}, parameters={self.parameters_required})>"


class ParameterPreset(Base):
    __tablename__ = "parameter_presets"

    id: Mapped[int] = mapped_column(primary_key=True)
    template_id: Mapped[int] = mapped_column(ForeignKey("recommendation_templates.id", ondelete="CASCADE"))
    match_criteria: Mapped[dict] = mapped_column(JSON)
    parameters: Mapped[dict] = mapped_column(JSON)

    def __str__(self):
        return f"<ParameterPreset (id={self.id}, template={self.template_id}, #parameters={len(self.parameters)}, values={self.dict()})>"

    def dict(self):
        return dict(sorted(self.match_criteria.items()))

    def matchKeys(self):
        return list(self.match_criteria.keys())


class RecommendationGenerated(Base):
    __tablename__ = "recommendations_generated"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))
    control_id: Mapped[int] = mapped_column(ForeignKey("security_controls.id", ondelete="CASCADE"))
    final_text: Mapped[str]
    generated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
