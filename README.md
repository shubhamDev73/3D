# Basic 3D modelling and rendering system

## Description

This is a very basic implementation of a 3D modelling and rendering system.

The Python module is used for creating 3D models and basic visualization of the 3D models made, and to export it to be used by the WebGL rendering module.

The exported 3D model is used in `webgl.html` and rendered using WebGL library for web browsers. This is used as it requires no installation (already built-in in most modern day browsers) while still exposing core graphics functionality such as transformations, lighting and shader coding.

3D model is exported as an array of vertices, indices referring to those vertices, and colors assigned to those vertices in a .js format to be used as variables in the `webgl.html` page.

## Installation and running

The python module of this program was written in `Python 3.7.4`, using tkinter library for creating the UI. This already comes in-built with most python installations.

WebGL is used for rendering the exported 3D model on the web browser, which comes in-built and is supported by most major browsers. [Click here](https://get.webgl.org/) to see if your browser supports WebGL or not.

To run the program, first run `python main.py` to create the 3D model. After creating the model, select it (selected model will appear as red), and press Export to export it in js format to be used by webgl module.

Then, open `webgl.html` page using a web browser which supports WebGL, to see the 3D model rendered live.

## Files

- **\_\_init\_\_.py** : to mark the folder and python files present in it as modules.
- **structs.py** : defines matrix and vector classes and common transformations used (such as translate, rotate and scale).
- **model.py** : defines the object class which is base class for any object present in the scene. Also defines model and camera classes which are a special case of the object class, and hence inherit from it.
- **scene.py** : defines the scene class which contains the entire 3D scene. It contains 1 camera to render the scene and a list of all models present in it.
- **render.py** : does transformations and projections so that all the models present in the scene can be viewed on the canvas defined in `ui.py`.
- **ui.py** : implements the UI used for the 3D modelling sub-system.
- **main.py** : starting point for running the 3D modelling sub-system.
- **model.js** : the exported 3D model used in `webgl.html`.
- **webgl.html** : HTML page used to render the 3D model using WebGL library.

## TO DO

- Implement rotation transformation.
- Correctly use the u, v, n vectors used in projection matrix.
- Implement visible surface detection algorithms to clip models and dislay only those parts which are in front.
- Improve the UI to incorporate model transformation, model editing and render options.
- Separate code files for vertex and fragment shaders.
