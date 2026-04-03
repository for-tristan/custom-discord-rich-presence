
# Discord Rich Presence 
<img width="40" height="80" alt="Adobe Express - file" src="https://github.com/user-attachments/assets/3589ce86-8cdf-4c89-8eb7-97b58ef41221" /> 

A GUI application to set and manage custom Discord Rich Presence statuses.

<img src="https://img.shields.io/badge/Python-3.8%2B-blue" />
<img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey" />

## Features

- Discord-authentic dark theme UI
- Live editing without restarting
- Optional image support

## Demo

![2026-04-0207-31-30-ezgif com-crop](https://github.com/user-attachments/assets/f0fe6d4e-7b14-404f-80c9-68f50492858f)
      
## Installation

 #### Git clone this Repo 
```sh
  git clone https://github.com/for-tristan/custom-discord-rich-presence
  cd custom-discord-rich-presence
  pip install -r requirements.txt
```
## Requirements


```bash
customtkinter>=5.2.0
pypresence>=4.2.0
```


    
## Usage
#### 1. Get an Application ID
- Go to Discord Developer Portal
- Create a new application or select existing one
- Copy the Application ID
#### 2. Run the app
```bash
python RPC.py
```
3. Set your presence
- Paste your Application ID
- Click Test Connection to verify
- Fill in Details and State
- Optionally add an image key (must be uploaded in your app's Rich Presence assets)
- hit Start
- Use Apply Changes to update while running

### Adding Images
#### 1. In your Discord application, go to Rich Presence → Art Assets
#### 2. Upload an image and note the key name
#### 3. Enter that key in the Image Key field

> [!IMPORTANT]
> - Discord must be running for the RPC to display
> - The timer starts when you click Start
> - Closing the app stops the presence automatically
