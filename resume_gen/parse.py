import datetime
import json
import logging
import shutil
import subprocess
import sys
import tempfile
from logging import FileHandler
from pathlib import Path

import click
import yaml

from resume_gen.schema import Resume
from resume_gen.template_renderer import TemplateType, render_resume
from resume_gen.util import omit_sensitive_info

logging_filename_datetime = datetime.datetime.now().isoformat()
logging_filename = f"resume-gen_{logging_filename_datetime}.log"
logging.basicConfig(
    level=logging.INFO, handlers=[FileHandler(filename=logging_filename, delay=True)]
)
logger = logging.getLogger()
logger.disabled = True


def build_pdf(tex_file: Path, build_dir: Path) -> Path:
    """Build PDF from LaTeX file using pdflatex in the specified directory."""
    logger.info(f"Building PDF from {tex_file} in {build_dir}")

    # Copy template dependencies if they exist
    template_dir = Path(__file__).parent
    for dep in template_dir.glob("*.sty"):
        shutil.copy(dep, build_dir)

    # Run pdflatex twice for proper references
    for i in range(2):
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-file-line-error",
                tex_file.name,
            ],
            cwd=build_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.error(f"pdflatex failed on pass {i+1}:\n{result.stdout}")
            # Read the log file for better error messages
            log_file = tex_file.with_suffix(".log")
            error_msg = "LaTeX compilation failed"
            if log_file.exists():
                with open(log_file) as f:
                    log_content = f.read()
                    # Extract error message - look for lines starting with '!'
                    errors = [
                        line.strip()
                        for line in log_content.split("\n")
                        if line.startswith("!")
                    ]
                    if errors:
                        error_msg = "\n".join(errors)

                    logger.error(f"pdflatex log:\n{log_content}")
            raise click.ClickException(
                f"PDF generation failed.\nLaTeX errors:\n{error_msg}"
            )

    pdf_file = tex_file.with_suffix(".pdf")
    if not pdf_file.exists():
        raise click.ClickException("PDF file was not created")

    return pdf_file


@click.command()
@click.argument("input", type=click.File("r"), default=sys.stdin)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    help=(
        "Output PDF file path."
        "If not specified, will use input filename with .pdf extension"
    ),
)
@click.option(
    "--omit-sensitive",
    is_flag=True,
    help="Censor sensitive information like phone numbers",
)
@click.option(
    "--keep-tex",
    is_flag=True,
    help="Keep the generated LaTeX file alongside the PDF",
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"], case_sensitive=False),
    help="Enable logging and set the log level",
)
@click.option(
    "--template",
    type=click.Choice(["resume", "cv"], case_sensitive=False),
    default="resume",
    help="Choose the template type to use (default: resume)",
)
def cli(
    input: click.File,
    output: str,
    omit_sensitive: bool,
    keep_tex: bool,
    log_level: str,
    template: str,
):
    """Generate a PDF resume from YAML or JSON input data.

    Read resume data from INPUT file (or stdin if not specified) and generate a PDF.
    Supports YAML and JSON formats.
    """
    if log_level:
        logger.setLevel(log_level.upper())
        logger.disabled = False
        logger.info("Logging enabled")

    # Parse input
    if input.name == "<stdin>":
        logger.debug("Reading from stdin")
        if sys.stdin.isatty():
            ctx = click.get_current_context()
            click.echo(ctx.get_help())
            ctx.exit()
        resume_raw = json.load(input)
    elif input.name.endswith((".yaml", ".yml")):
        logger.debug(f"Reading YAML: {input.name}")
        resume_raw = yaml.safe_load(input)
    elif input.name.endswith(".json"):
        logger.debug(f"Reading JSON: {input.name}")
        resume_raw = json.load(input)
    else:
        raise click.BadParameter(
            f"Unsupported file type: {input.name}. Use .yaml, .yml, or .json"
        )

    # Validate and process resume data
    resume = Resume.model_validate(resume_raw)
    if omit_sensitive:
        resume = omit_sensitive_info(resume)

    # Determine output path
    if not output:
        if input.name == "<stdin>":
            output = f"{template}.pdf"
        else:
            output = str(Path(input.name).with_suffix(".pdf"))

    # Create temporary build directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        logger.debug(f"Created temporary directory: {tmp_path}")

        # Generate LaTeX in temp dir
        tex_file = tmp_path / f"{template}.tex"
        render_resume(resume, str(tex_file), TemplateType(template))
        logger.info(f"Generated LaTeX file: {tex_file}")

        # Build PDF
        pdf_file = build_pdf(tex_file, tmp_path)
        logger.info(f"Generated PDF file: {pdf_file}")

        # Copy results to final destination
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf_file, output_path)
        logger.info(f"Copied PDF to: {output_path}")

        if keep_tex:
            tex_output = output_path.with_suffix(".tex")
            shutil.copy2(tex_file, tex_output)
            logger.info(f"Kept LaTeX file at: {tex_output}")


if __name__ == "__main__":
    cli()
