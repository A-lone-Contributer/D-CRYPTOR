<!-- PROJECT SHIELDS -->
<code>[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)</code>
<code>[![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)](https://forthebadge.com)</code>
<code>[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)</code>

![Product Name Screen Shot][product-screenshot]

<hr>
<p>
  <p align="center">
    A Command line tool for Cipher Decryption using Genetic Algorithms and Natural Language Processing (NLP).
    <br />
    <br />
    <a href="https://github.com/A-lone-Contributer/D-CRYPTOR/issues">Report Bug</a>
    </p>
</p>

<hr>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Ever thought how Natural language processing can be used for decryption of a cipher text? Well, here is the answer!

**D-CRYPTOR** is capable of encrypting and decrypting cipher text using **Genetic Algorithm** and **Natural language processing (NLP).**

> **Key Idea :** After learning the probability likelihoods of normal english text, we can mutate the cipher (swapping) to minimize the difference of
probability likelihood to plain english text. This mutation would be closed to the original mapping thus deciphered text.

**High level Overview :**
1. A encoded text is generated using a **random character-character mapping** (source : <code>encoder.py</code>)
2. Now, for the decoding purpose following steps are performed:
    * A **Markov Matrix** of bi-grams probabilities is generated from the training data <code>train.txt</code>.
    * We extend this to generate probabilities for the whole sequence and normalise to range (0,1).
    * Now, generate random pool of **DNA** (a list of lowercase ascii characters) and shuffle them.
    * To mutate, we take few candidates from the pool and generate probability score till number of iterations or out best score doesn't improve.
3. Now, we use this best likelihood score character mapping and apply to cipher text and obtain deciphered sentence.
4. To make decryption process interesting, script uses <code>truecasing.py</code> which tries to reterive the original casing of decyphered text without knowing of it in the first place.

**LIMITATIONS** 

1. D-CRYPTOR cannot decrypt sentences with very few words as a 26 character mapping is harder to learn from it.
2. Being a randomized algorithm, it might be possible that you get different result on successive runs.
3. Does not decode punctuations.

<hr>

### Built Using
* [Python](https://www.python.org/)
* [NLTK](https://www.nltk.org/)
* [curses](https://docs.python.org/3/library/curses.html)

<hr>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

1. **Python**

To check, if python is installed, type <code>python</code> in command line. If this opens <code>python3</code> interpreter then you are good to go. 

else, <code>python3</code> follow [this](https://www.python.org/downloads/) link to download the latest version.

2. **Git**

You can download the latest version of <code>git</code> [here](https://git-scm.com/downloads).

### Installation

1. Clone the repo

```sh
git clone https://github.com/A-lone-Contributer/D-CRYPTOR.git
```
2. Install the dependencies

```sh
pip install -r requirements.txt
```

3. Download <code>distributions.obj</code> file which is a dependency of <code>truecasing.py</code> using [this](https://github.com/nreimers/truecaser/releases/download/v1.0/english_distributions.obj.zip) link. Extract the downloaded file and place it in the script directory.

<hr>

<!-- USAGE EXAMPLES -->
## Usage

1. To run D-CRYPTOR, run the <code>master.py</code> file.

```sh
python master.py
```
NOTE: If <code>python master.py</code> does not work, try using <code>python3 master.py</code> instead.

2. A intro splash screen would be displayed that looks something like this:

> NOTE: You can press <code>Enter</code> to skip the animation screen.

![Product Splash][product-splash]


3. Now, you will be directed to a menu. Choose the first option (if not done before)

![Product Menu][product-menu]

4. After selecting the first option, you will be given a text box where you can write your original message which you want to
encode and decode. You can either type of paste the copied text.

> NOTE: Follow prompts written on the top of text field.

![Encyption Input][encryption-input]

5. Press <code>CTRL+G</code> to execute and obtain the encrypted message. This message is also saved in a text file named <code>encoded_text.txt</code>.
After encryption, the cipher will look something like this

![Encrypted Output][encryption-output]

6. As, we have generated the encrpted text, we can directly decypher the text. So, navigate to the decryption option on the menu and press <code>Enter</code>. A splash screen like this will be displayed.

![Decryption Splash][decryption-splash]

7. Final decoded text will be displayed after sometime. 

> NOTE: Running time of the algorithm depends on PC Specs and the length of the plain text being deciphered.


![Decryption Output][decryption-output]


<hr>

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/A-lone-Contributer/D-CRYPTOR/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the Apache-2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Nishkarsh Tripathi : nishkarsh78@gmail.com

Project Link : [D-CRYPTOR](https://github.com/A-lone-Contributer/D-CRYPTOR)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[issues-shield]:	https://img.shields.io/github/issues/A-lone-Contributer/D-CRYPTOR
[issues-url]: https://github.com/A-lone-Contributer/D-CRYPTOR/issues
[forks-shield]: https://img.shields.io/github/forks/A-lone-Contributer/D-CRYPTOR
[forks-url]: https://github.com/A-lone-Contributer/D-CRYPTOR/network/members
[stars-shield]: https://img.shields.io/github/stars/A-lone-Contributer/D-CRYPTOR
[stars-url]: https://github.com/A-lone-Contributer/D-CRYPTOR/stargazers
[license-shield]: https://img.shields.io/github/license/A-lone-Contributer/D-CRYPTOR
[license-url]: https://github.com/A-lone-Contributer/D-CRYPTOR/blob/main/LICENSE
[product-screenshot]: images/logo.png
[product-splash]: images/Splash.png
[product-menu]: images/main.png
[encryption-input]: images/encrypt_input.png
[encryption-output]: images/encoded_output.png
[decryption-splash]: images/decrypt_splash.png
[decryption-output]: images/decoded_output.png
