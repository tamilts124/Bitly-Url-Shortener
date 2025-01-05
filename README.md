# Free Bitly URL Shortener

A Python script that allows you to create unlimited Bitly short URLs quickly and efficiently. This tool supports both free and user-authenticated shortening options. The Bitly Account Generator is also available in our [repository](https://github.com/tamilts124/Bitly-Url-Shortener).

## Features

- **Free URL Shortening**: Create short URLs anonymously without an account.
- **Authenticated URL Shortening**: Use your Bitly account for more flexibility and to bypass rate limits.
- **Efficient Workflow**: Handles requests and responses effectively with detailed error handling.
- **Easy to Use**: Simple command-line interface for creating and managing short URLs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tamilts124/Bitly-Url-Shortener.git
   cd Bitly-Url-Shortener
   ```
2. Install the required dependencies:
   ```bash
   pip install requests optparse
   ```

## Usage

Run the script with the following options:

### Free URL Shortening
To shorten a URL without an account:
```bash
python Bitly-Url-Shortener.py -l <LONG_URL>
```
Example:
```bash
python Bitly-Url-Shortener.py -l https://example.com
```

### Authenticated URL Shortening
To shorten a URL using a Bitly account:
```bash
python Bitly-Url-Shortener.py -l <LONG_URL> -a <ACCOUNT> -p <PASSWORD>
```
Example:
```bash
python Bitly-Url-Shortener.py -l https://example.com -a myemail@example.com -p mypassword
```

## Command-Line Options

| Option       | Description                              | Required | Example                     |
|--------------|------------------------------------------|----------|-----------------------------|
| `-l, --longurl` | The URL to shorten.                     | Yes      | `-l https://example.com`    |
| `-a, --account` | Bitly account email/username.           | Optional | `-a myemail@example.com`    |
| `-p, --password` | Bitly account password.                 | Optional | `-p mypassword`             |

## Error Handling

- **INVALID_ARG_URL**: Ensure the provided URL is valid.
- **RATE_LIMIT_EXCEEDED**: Retry later or use an authenticated account.
- **USER ACCOUNT NOT FOUND**: Verify your account credentials.

## How It Works

1. **Free URL Shortening**:
   - Uses the anonymous shortening endpoint provided by Bitly.
   - Limited by rate restrictions.

2. **Authenticated URL Shortening**:
   - Logs into your Bitly account.
   - Retrieves the `group_guid` for URL shortening.
   - Sends a request to the authenticated shortening API to create a short URL.

## Related Repository

- **Bitly Account Generator**: [Generate Bitly accounts quickly](https://github.com/tamilts124/Bitly-Url-Shortener).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

*Contributions and feedback are welcome!*

