# MakeCents: A dialogue system for coin collectors

![makecents_logo](MakeCents_logo.png)

<!-- Font for logo is IM Fell English SC from google price_utilities price_utilities.google.com/specimen/IM+Fell+English+SC -->
<!-- Coin graphic from https://etc.usf.edu/clipart/44400/44401/44401_penny.htm -->

MakeCents is a dialogue system designed to help coin collectors quickly query coin prices. 

MakeCents is currently under development. Check back in a few days for an initial release

## Installation and Testing Instructions

1. Activate environment

2. `pcgs_scraper` package
	1. download the latest release at `https://github.com/ryanamannion/pcgs_scraper/releases`
	2. `pip install path/to/pcgs_scraper-X.Y.Z.tar.gz`

3. Other dependencies
	1. `pip install -r requirements.txt`
	2. `pip list | grep rasa` should reveal:
		* `rasa 2.1.3`
		* `rasa-x`
		* `rasa-sdk`

4. Change directories to `makecents`

5. make the `makecents-test` shell script executable with `chmod +x makecents-test`

6. run makecents-test with `./makecents-test`

7. On the left-hand side, navigate to `Talk to your bot`, and start chatting with MakeCents

7. To quit, close the Rasa X tab, go back to the shell, exit with `CTRL+C`
