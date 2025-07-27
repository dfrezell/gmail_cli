# Email CLI

A Python command-line interface for sending emails through Gmail API or Outlook/Microsoft Graph API.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up email provider credentials:

### Gmail Setup
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API
   - Create OAuth 2.0 credentials (Desktop application)
   - Download the credentials as `credentials.json` and place it in this directory

### Outlook Setup
   You need to create an Azure app registration for Outlook.com accounts:
   
   1. Go to the [Azure Portal](https://portal.azure.com/)
   2. Navigate to "App registrations" > "New registration"
   3. Set the following:
      - **Name**: Give it a name like "Email CLI"
      - **Supported account types**: Select "Personal Microsoft accounts only"
      - **Redirect URI**: Leave blank (we'll use device code flow)
   4. After creation, go to "Manage" > "Authentication" > "Settings" and:
      - Check "Allow public client flows" at the bottom
      - Click "Save"
   5. Go to "Manage" > "API permissions" and:
      - Click "Add a permission"
      - Select "Microsoft Graph" > "Delegated permissions"
      - Add "Mail.Send" permission
      - Click "Grant admin consent" (if you're an admin) or have an admin approve it
   6. Copy the "Application (client) ID" from the Overview page
   7. Create a file named `outlook_client_id.txt` in this directory and paste the client ID into it

## Usage

The CLI automatically detects the email provider based on the sender's email domain, or you can force a specific provider with the `--provider` flag.

### Basic usage with HTML and text files:
```bash
python gmail_cli.py --from sender@gmail.com --to recipient@example.com --subject "Test Subject" --html message.html --text message.txt
```

### Force specific provider:
```bash
python gmail_cli.py --from sender@outlook.com --to recipient@example.com --subject "Test Subject" --html message.html --provider outlook
```

### With attachments:
```bash
python gmail_cli.py --from sender@gmail.com --to recipient@example.com --subject "Test Subject" --html message.html --attachments file1.txt file2.pdf
```

## Arguments

- `--from`: Sender email address (required)
- `--to`: Recipient email address (required)
- `--subject`: Email subject (required)
- `--html`: HTML file to use as email body (required)
- `--text`: Text file to use as email body (optional)
- `--provider`: Force specific email provider: `gmail` or `outlook` (optional, auto-detected if not specified)
- `--attachments`: File paths to attach (optional)

## Provider Auto-Detection

The CLI automatically detects the email provider based on the sender's domain:

- **Gmail**: gmail.com, googlemail.com
- **Outlook**: outlook.com, hotmail.com, live.com, msn.com
- **Default**: Gmail (for unknown domains)

## First Run

### Gmail
On the first run, you'll be prompted to authenticate via your browser. This will create a `token.pickle` file for future authentication.

### Outlook
On the first run, you'll be prompted to authenticate using device code flow. Visit the provided URL and enter the device code. This will create an `outlook_token.pickle` file for future authentication.

## EML Message Parser

The repository also includes a utility to parse EML files and extract HTML/text content:

```bash
python decode_messages.py
```

This will read `message.eml` and extract the content into `message.html` and `message.txt` files with proper UTF-8 encoding.