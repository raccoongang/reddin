# Reddin X-Block for edX Platform


## Overview

The Reddin X-Block is a custom X-Block designed for Reddin integration with the edX platform. It provides 
a seamless way to incorporate interactive polls and quizzes Reddin into your edX courses.

## Installation

To install the Reddin X-Block on your edX platform, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/raccoongang/reddin.git
    ```

2. Navigate to the `reddin` directory:

    ```bash
    cd reddin
    ```

3. Install the X-Block:

    ```bash
    pip install .
    ```

4. Restart the edX platform.

5. Add `reddin` to the Advanced Module List in your course Advanced Settings.

## Usage

Once installed and enabled, you can add the Reddin X-Block to your edX courseware. 
Follow these steps to incorporate polls or quizzes into your course:

1. Navigate to the unit where you want to add the Reddin X-Block.
2. Click on the "Advanced" button in "Add New Component" .
3. Select "Reddin XBlock" from the list of available components.
4. In the X-Block settings, you need to add a link to the required iframe in the "Reddin URL" field, 
and if the link contains GET parameters, they should be added to the corresponding field in json format.
5. Save your changes and preview the X-Block in the courseware.

___
### **Important!**

**For correct operation, you need to add `REDDIN_SECRET_KEY` to the settings.**

**The LMS and Studio urls must be added to the CORS whitelist on the site side of the iframe used in the block, 
or the site and LMS and Studio must be on the same domain to share cookies.**
