# Basic 3D modelling and rendering system

## Description

This is a very basic implementation of a 3D modelling and rendering system.

The entire system is divided into 2 sub-systems: **3D modelling sub-system** and **rendering sub-system**.

**Python** language is used for creating the 3D modelling sub-system, which creates 3D models and provides basic visualization of those models, and exports it to be used by the rendering sub-system.

**WebGL** graphics library is used in the rendering sub-system to render the exported 3D model in web browsers. This is used as it requires no installation (already built-in in most modern day browsers) while still exposing core graphics functionality such as transformations, lighting and shader coding.

3D model is exported as an array of vertices, indices referring to those vertices, and colors assigned to those vertices in a **js format** to be used as variables in the `webgl.html` page.

## Installation and running

The python module of this program was written in `Python 3.7.4`, using **tkinter** library for creating the UI. This already comes built-in with python 3 installations.

`WebGL` is used for rendering the exported 3D model on the web browser, which is supported by most major browsers and comes in-built. [Click here](https://get.webgl.org/) to see if your browser supports WebGL or not.

To run the program, first run `python main.py` and create a 3D model. After creating the model, select it (selected model will appear as **red**), and press `Export` to export it in js format to be used by rendering sub-system.

Then, open `webgl.html` page using a web browser which supports WebGL, to see the 3D model rendered live.

## Files

1. 3D modelling sub-system
   - **\_\_init\_\_.py** : to mark the folder and python files present in it as modules.
   - **structs.py** : defines matrix and vector classes.
   - **model.py** : defines the object class which is base class for any object present in the scene. Also defines model and camera classes which are a special case of the object class, and hence inherit from it.
   - **scene.py** : defines the scene class which contains the entire 3D scene. It contains 1 camera to render the scene and a list of all models present in it.
   - **render.py** : does transformations and projections so that all the models present in the scene can be viewed on the canvas defined in `ui.py`.
   - **ui.py** : implements the UI used for the 3D modelling sub-system.
   - **main.py** : starting point for running the 3D modelling sub-system.

2. Exported 3D model
   - **model.js** : the exported 3D model used in `webgl.html`.

3. Rendering sub-system
   - **webgl.html** : HTML page used to render the 3D model using WebGL library. This is currently the only file used in the rendering sub-system.

## TO DO

1. 3D modelling sub-system
   - Implement camera rotation and hence correctly use the u, v, n vectors used in projection matrix.
   - Implement visible surface detection algorithms to clip models and display only those parts which are in front.
   - Incorporate model editing options.
   - Implement material as a different class rather than a tuple of color values.
   - Add material selection to model and individual faces.
   - Add lights and export them in correct format.
   - Implement rendering algorithm.

2. Rendering sub-system
   - Separate code files for vertex and fragment shaders.
   - Support for multiple objects.
   - Implement lighting and shadow.
