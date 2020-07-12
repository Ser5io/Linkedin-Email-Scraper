# Linkedin-Email-Scraper
Give it a search URL, it will give you the emails of the profiles (if they have emails) in a csv file

## Installation (Windows)
### 0- Prerequisits
Download [Google Chrome](https://www.google.com/chrome/) if you don't have it already.

### 1- Download the *Linkedin Email Scraper* (exe) from [release](https://github.com/Ser5io/Linkedin-Email-Scraper/releases/tag/v1.0)
### 2- Open command prompt and enter this command
```
reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version
```
You should get something like this
```
HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon
    version    REG_SZ    83.0.4103.116
```
### 3- Download corresponding chromedriver.exe
Go to [this download page](https://chromedriver.chromium.org/downloads).
Under current releases, download the version of chromedriver.exe you got in the previous step.

### 4- Put the files in the same directory
Move the chromedriver.exe and the app downloaded into the same directory for the app to work.
