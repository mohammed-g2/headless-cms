# Flask Project Template

### Suggested commands
- install virtual environment `python -m venv .venv`
- activate environment: `.venv\Scripts\activate`
- update pip and setuptools: `python.exe -m pip install --upgrade pip setuptools`
- install poetry: `pip install poetry`


### Testing

#### Local email server
- install aiosmtpd: `pip install aiosmtpd`
- run: `aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025`
