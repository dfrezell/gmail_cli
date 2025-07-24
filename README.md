# Gmail CLI

A Python command-line interface for sending emails through the Gmail API.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up Gmail API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials as `credentials.json` and place it in this directory

## Usage

```bash
python gmail_cli.py --from sender@gmail.com --to recipient@example.com --subject "Test Subject" --message "Hello, World!"
```

### With attachments:
```bash
python gmail_cli.py --from sender@gmail.com --to recipient@example.com --subject "Test Subject" --message "Hello, World!" --attachments file1.txt file2.pdf
```

## Arguments

- `--from`: Sender email address (required)
- `--to`: Recipient email address (required)
- `--subject`: Email subject (required)
- `--message`: Email message body (required)
- `--attachments`: File paths to attach (optional)

## First Run

On the first run, you'll be prompted to authenticate via your browser. This will create a `token.pickle` file for future authentication.