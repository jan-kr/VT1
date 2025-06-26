from services import recommendation_generator_service, mode_handler
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="CLI Implementation Guideline Generator", )
    parser.add_argument("-m", "--mode", choices=['backup'])
    parser.add_argument("-f", "--file")
    parser.add_argument("-o", "--output", choices=['pdf', 'html'], default='html')
    args = parser.parse_args()

    match args.mode:
        case "backup":
            context = mode_handler.mode_backup(args.file)

            output = recommendation_generator_service.render_full(context=context, title="Backup Manual")
            recommendation_generator_service.save(content=output, output=args.output, filename=args.file)

        case _:
            print("No mode")
