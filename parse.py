import toml
import pprint
import jinja2
from jinja2 import Template
import os
import subprocess
import argparse


def escape_latex(val):
    return val.replace("~", "$\sim$").replace("%", "\%")

def format_list(input_list):
    return ", ".join([str(item) for item in input_list])

def write_rendered_tex_doc(cv_dict, output_filepath):
	rendered = template.render(data=cv_dict)
	with open(output_filepath, "w") as f:
		f.write(rendered)

if __name__ == "__main__":
	CV_DATA_FILEPATH = "cv.toml"
	LATEX_DOCUMENT_DIR = "./documents"

	latex_jinja_env = jinja2.Environment(
		block_start_string="\BLOCK{",
		block_end_string="}",
		variable_start_string="\VAR{",
		variable_end_string="}",
		comment_start_string="\#{",
		comment_end_string="}",
		line_statement_prefix="%%",
		line_comment_prefix="%#",
		trim_blocks=True,
		autoescape=False,
		loader=jinja2.FileSystemLoader(os.path.abspath("./documents")),
	)
	latex_jinja_env.filters["latexescape"] = escape_latex
	latex_jinja_env.filters["format_list"] = format_list

	template = latex_jinja_env.get_template('short_resume_template.tex')

	parser = argparse.ArgumentParser(description="Parses a TOML file and renders it as a LaTeX PDF")
	parser.add_argument('-f', '--full', action="store_true", help="Produce a full CV instead of an abbreviated resume")
	#parser.add_argument('-o', '--output', type=str,help="Optional output")

	args = parser.parse_args()

	if args.full:
		template = latex_jinja_env.get_template("cv.tex")

	cv_dict = toml.load("cv.toml")

	write_rendered_tex_doc(cv_dict, f"{LATEX_DOCUMENT_DIR}/temp_output.tex")

	cmd = "pdflatex -output-directory={} temp_output.tex".format(
			os.path.abspath("output")
	)
	subprocess.call(cmd, shell=True, cwd=LATEX_DOCUMENT_DIR)
