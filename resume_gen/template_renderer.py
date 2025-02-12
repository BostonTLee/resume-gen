import os
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from resume_gen.schema import Resume

def format_date_range(start_date, end_date):
    def format_date(raw_date):
        return raw_date.strftime("%b %Y")

    if end_date is None:
        end_date_str = "Present"
    else:
        end_date_str = format_date(end_date)
    start_date_str = format_date(start_date)
    return f"{start_date_str} -- {end_date_str}"

def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    chars = {
        '%': '\\%',
        '&': '\\&',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '~': '\\textasciitilde{}',
        '^': '\\textasciicircum{}',
        '\\': '\\textbackslash{}'
    }
    return ''.join(chars.get(c, c) for c in str(text))

def prepare_resume_data(resume: Resume):
    """Convert Resume model into a dict suitable for template rendering."""
    data = resume.model_dump()
    
    # Add formatted date ranges to jobs
    if data.get('work'):
        for job in data['work']:
            job['date_range'] = format_date_range(
                job['start_date'], 
                job.get('end_date')
            )
            # Escape special characters in job descriptions
            if job.get('description'):
                for bullet in job['description']:
                    bullet['content'] = escape_latex(bullet['content'])
    
    # Add formatted date ranges to education
    if data.get('education'):
        for edu in data['education']:
            edu['date_range'] = format_date_range(
                edu['start_date'],
                edu.get('end_date')
            )
            if edu.get('honors'):
                edu['honors'] = escape_latex(edu['honors'])
    
    # Escape special characters in other fields if needed
    if data.get('languages'):
        data['languages'] = [escape_latex(lang) for lang in data['languages']]
    if data.get('tools'):
        data['tools'] = [escape_latex(tool) for tool in data['tools']]
    
    return data

def render_resume(resume: Resume, output_file: str):
    """Render resume data into LaTeX using the template."""
    # Find the template relative to the package root
    package_root = Path(__file__).parent.parent
    templates_dir = package_root / 'templates'
    
    # Setup Jinja environment with LaTeX-friendly delimiters
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>',
        trim_blocks=True,
        lstrip_blocks=True,
    )
    
    # Get template
    template = env.get_template('resume.tex.j2')
    
    # Prepare data
    data = prepare_resume_data(resume)
    
    # Render template
    rendered = template.render(**data)
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(rendered)
    
    return output_file
