import logging
import datetime
import sys
import json
import yaml

from logging import FileHandler

import click

from schema import Resume
from latex_visitor import LatexVisitor


logging_filename_datetime = datetime.datetime.now().isoformat()
logging_filename = f"resume-gen_{logging_filename_datetime}.log"
logging.basicConfig(
    level=logging.INFO, handlers=[FileHandler(filename=logging_filename, delay=True)]
)
logger = logging.getLogger()
logger.disabled = True


@click.command()
@click.argument("file", required=False, type=click.File("r"), default=sys.stdin)
@click.option(
    "--output-file-base",
    required=False,
    default=None,
    help="The basename of the resulting file",
)
@click.option(
    "--log-level",
    required=False,
    default=None,
    help="Enable logging and set the log level",
)
def cli(file: click.File, output_file_base: str, log_level: bool):
    if log_level is not None:
        logger.setLevel(log_level.upper())
        click.echo(f"Logging to {logging_filename}", err=True)
        logger.disabled = False
        logger.info("Logging enabled")
    if file.name == "<stdin>":
        logger.debug("File is stdin")
        if sys.stdin.isatty():
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
            ctx.exit()
        resume_raw = json.load(file)
    elif file.name.endswith("yaml"):
        logging.debug(f"File is yaml: {file.name}")
        resume_raw = yaml.safe_load(file)
    elif file.name.endswith("json"):
        logging.debug(f"File is json: {file.name}")
        resume_raw = json.load(file)
    else:
        logging.error(f"File type unrecognized: {file.name}")
        click.echo(
            f"Unexpected file type for: {file.name}. Supported types: YAML, JSON"
        )
        sys.exit(1)
    resume = Resume.model_validate(resume_raw)
    latex_visitor = LatexVisitor(output_file_base)
    latex_visitor.visitResume(resume)


if __name__ == "__main__":
    cli()
