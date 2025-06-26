from jinja2 import Environment, FileSystemLoader

import pdfkit


def render_scenario(scenario, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(f"{scenario}.html.j2")

    manual = template.render(context)

    return manual


def render_full(context, title):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("base.html.j2")

    manual = template.render({
        "content": context,
        "title": title,
    })

    return manual


def save_html(content, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)


def save_pdf(html, filename):
    pdfkit.from_string(html, filename)


def save(content, output, filename):
    match output:
        case "pdf":
            save_pdf(content, filename + ".pdf")
        case _:
            save_html(content, filename + ".html")
