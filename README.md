# gmail_rule_runner
Small Project to Run Rules in Gmail


# **Installation**
Download tar or directly install using git url

## Direct Install
Execute command `pip install git+https://github.com/prabhakaran1021/gmail_rule_runner.git`

### Video Example:
[![Direct_Install](https://res.cloudinary.com/marcomontalbano/image/upload/v1685469203/video_to_markdown/images/google-drive--1B1bjOqvSLAHlpCqBMer4-6jIy7nMcpXR-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://drive.google.com/file/d/1B1bjOqvSLAHlpCqBMer4-6jIy7nMcpXR/view?usp=share_link "Direct_Install")

## Download Tar
[![Tar_Install](https://res.cloudinary.com/marcomontalbano/image/upload/v1685469278/video_to_markdown/images/google-drive--1nkrkLOA3z2GwDnULrd2zbjS9B5aeet1f-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://drive.google.com/file/d/1nkrkLOA3z2GwDnULrd2zbjS9B5aeet1f/view?usp=share_link "Tar_Install")

1. Download Tar file or wheel file from [here](https://github.com/prabhakaran1021/gmail_rule_runner/releases/tag/0.0.1)<br> 
2. Execute command `pip install "downloaded_file_location"`<br>

### Video Example:

## AUTH
Authenticated using oauth2 credentials generated from Google Cloud Console. Download the credentials file and save as json file.<br>
Authentication is required only for first call.If successful. Token is saved in a pickle file which can be reused till it is expired.Auth tokens are refreshed if they are expired.
# How to Use:

## Video Tutorial

### Note: 
All actions are done in a batch of 100 to avoid gmail api limit exception


