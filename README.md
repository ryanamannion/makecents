# MakeCents: A dialogue system for coin collectors

![makecents_logo](MakeCents_logo.png)

<!-- Font for logo is IM Fell English SC from google price_utilities price_utilities.google.com/specimen/IM+Fell+English+SC -->
<!-- Coin graphic from https://etc.usf.edu/clipart/44400/44401/44401_penny.htm -->

MakeCents is a dialogue system designed to help coin collectors quickly query coin prices. 

MakeCents is currently under development. Check back in a few days for an initial release

## Installation and Testing Instructions

1. `cd` into the topmost dir of this repo, `makecents`

2. Create/ activate your environment

3. `pcgs_scraper` package
	1. make `latest_releases` executable with `chmod +x latest_releases`
	2. run `./latest_releases`
	3. install latest version with `pip install pcgs_scraper-releases/pcgs_scraper-vX.Y.Z.tar.gz`

4. Other dependencies
	1. `pip install -r requirements.txt`
	2. `pip list | grep rasa` should reveal:
		* `rasa 2.1.3`
		* `rasa-x`
		* `rasa-sdk`

5. Change directories to `./makecents/`

6. make the `makecents-test` shell script executable with `chmod +x makecents-test`

7. run `./makecents-test`

8. On the left-hand side, navigate to `Talk to your bot`, and start chatting with MakeCents

9. To quit, close the Rasa X tab, go back to the shell, exit with `CTRL+C`
