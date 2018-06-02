# Ulauncher Sentry

> [ulauncher](https://ulauncher.io/) Extension to easy access your [Sentry](https://sentry.io) projects.

## Usage

![demo](demo.gif)

## Requirements

* [ulauncher](https://ulauncher.io/)
* Python >= 2.7
* A [Sentry](https://sentry.io) account.

## Install

Open ulauncher preferences window -> extensions -> add extension and paste the following url:

```https://github.com/brpaz/ulauncher-sentry```

## Usage

* Before usage you need to configure your Sentry "auth_token" in plugin preferences.
* The results from the Sentry API are cached by 1h.
 
## Development

```
git clone https://github.com/brpaz/ulauncher-sentry
cd ~/.cache/ulauncher_cache/extensions/ulauncher-sentry
ln -s <repo_location> ulauncher-sentry
```

To see your changes, stop ulauncher and run it from the command line with: ```ulauncher -v```.

## License 

MIT
