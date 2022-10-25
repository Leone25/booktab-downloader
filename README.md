# booktab-downloader

A python script to download you Zanichelli books from web Booktab as PDFs, now updated!

**NOTE:** this doesnt work for the kitaboo reader (new web reader), to download those please look at https://github.com/Leone25/kitaboo-downloader

## How to use

NOTE: Often chromium browsers (Eg. chrome, edge ...) don't always show the cookie for whatever reason. Please use firefox, and remember to enable "show raw headers" otherwise the cookie will be shortened and you will receive an error.

1. Download this repo, unzip the download, open a terminal, navigate to the extracted files and type:
   
   ```bash
   pip install -r requirements.txt
   ```

2. Run the script with python3

3. Open [Booktab Web](http://web-booktab.zanichelli.it/) and login

4. Open the developers tool, go in the "network" tab and enable the `Fetch/XHR` filter and disable cache

5. Click on the cover of the volume you'd like to download in the booktab page

6. Back in the network tools look for the `volume.xml` or `spine.xml` file that should appear in the network tab

7. Select it and scroll down to the boottom of the headers where it says `Cookie`

8. If you're on macOS: paste the cookie in the cookies.txt file, otherwise copy all the cookies (do not include the `Cookie:` part) and paste them in the terminal and press enter

9. Take the ISBN of the book you'd like to download, paste it into the terminal and press enter

10. The script will now begin downloading the book, the amount of time it takes to do everything depends on your internet speed and the size of the book

11. After the download is done it will ask for a file name, write the name of the book and press enter

12. Now you have a .pdf in the same directory of the script, enjoy!

NB: Some times one IBSN might refer to multiple books, in that case look for the IBSN in the url, it's in the url.

## Disclaimer

Remember that you are responsible for what you are doing on the internet and even tho this script exists it might not be legal in your country to create personal backups of books.

I may or may not update this script depending on my needs, but I'm open to pull requests ecc.

## License

This software uses the MIT License
