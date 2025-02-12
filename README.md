# Resume Generator

A Python tool to generate clean LaTeX resumes from structured YAML or JSON data.

## Installation

```bash
pip install .
```

This will install the `resume` command-line tool and all dependencies.

## Usage

Basic usage:
```bash
resume input.yaml -o output.pdf
```

Using with stdin/pipe:
```bash
yq -o json '.work[] | select(.employer=="Google")' cv.yaml | resume -o google_resume.pdf
```

### Options

- `-o, --output`: Output PDF file path (default: input filename with .pdf extension)
- `--omit-sensitive`: Censor sensitive information like phone numbers
- `--keep-tex`: Keep the generated LaTeX file alongside the PDF
- `--log-level`: Enable logging and set log level (DEBUG, INFO, WARNING, ERROR)

### Input Format

Supports both YAML and JSON input through files or stdin. Example YAML format:

```yaml
profile:
  name: "John Doe"
  email: "john.doe@example.com"
  phone: "(123) 456-7890"
  linkedin: "https://linkedin.com/in/johndoe"
  site: "https://johndoe.com"

work:
  - title: "Senior Software Engineer"
    employer: "Tech Corp"
    location: "San Francisco, CA"
    start_date: "2020-01-01"
    end_date: "2023-12-31"
    description:
      - content: "Led development of core platform features"
      - content: "Improved system performance by 50%"
```

See `test_resume.yaml` for a complete example.

## Requirements

- Python 3.8+
- LaTeX distribution (e.g., TexLive)

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## License

MIT License
