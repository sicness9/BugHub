<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">BugHub</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/sicness9/BugHub"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/sicness9/BugHub">View Demo</a>
    ·
    <a href="https://github.com/sicness9/BugHub/issues">Report Bug</a>
    ·
    <a href="https://github.com/sicness9/BugHub/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

LINK: https://bughub-nelson.herokuapp.com/

My first big project, BugHub. It was built primarily with Python and is a bug/task tracker.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* Python
* Flask
* HTML
* Auth0 integration for the sign in/authentication
* SendGrid API for emails

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip
  ```sh
  py -m ensurepip --upgrade
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/sicness9/BugHub.git
   ```
2. Install PIP packages
   ```sh
   pip install -r requirements.txt
   ```
3. Get your SendGrid API from sendgrid.com
4. Enter your API in .env
   ```py
    SENDGRID_API_KEY= 'ENTER YOUR API KEY'
   ```
5. Sign up for Auth0 and get API keys and secrets
6. Enter Auth0 informatin in .env
   ```py
   DOMAIN= 
   API_AUDIENCE= 
   ALGORITHMS= 
   ISSUER= 
   CLIENT_SECRET=
   CLIENT_ID=
   API_BASE_URL=
   ACCESS_TOKEN_URL=
   AUTHORIZE_URL=
   ```
   

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Allows for creating teams and from the teams dashboard, can see the activity per each department.

![Teams dashboard image](https://i.imgur.com/vhd9TwY.png)


Once a team is created, users can invite team members. User's can invite multiple emails at once (comma separated)

![Team invite members](https://i.imgur.com/1azWWCf.png)

The core functionality of this app is to be a task/bug tracker. From this dashboard, you can see a list of all the tickets and their status

![Bug Dashboard](https://i.imgur.com/llckU6R.png)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Nelson Torres - mrnelsontorres@gmail.com

Project Link: [https://github.com/sicness9/BugHub](https://github.com/sicness9/BugHub)

<p align="right">(<a href="#top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/sicness9/BugHub.svg?style=for-the-badge
[contributors-url]: https://github.com/sicness9/BugHuB/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/sicness9/BugHub.svg?style=for-the-badge
[forks-url]: https://github.com/sicness9/BugHub/network/members
[stars-shield]: https://img.shields.io/github/stars/sicness9/BugHub.svg?style=for-the-badge
[stars-url]: https://github.com/sicness9/BugHub/stargazers
[issues-shield]: https://img.shields.io/github/issues/Sicness9/BugHub.svg?style=for-the-badge
[issues-url]: https://github.com/Sicness9/BugHub/issues
[license-shield]: https://img.shields.io/github/license/Sicness9/BugHub.svg?style=for-the-badge
[license-url]: https://github.com/Sicness9/BugHub/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/nelson-torres-905153209
[product-screenshot]: images/screenshot.png
