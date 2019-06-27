# ShapeRecognition

Hopfield network implemented with Python.

## Requirement

- Python3     for  _train.py
- Python2.7   for example.py
- numpy
- matplotlib
- tqdm
- PIL
- cv2

## Usage

Run `_train.py`.

## Demo

### _train.py

The following is the result of using **Asynchronous** update.

```bash
Start to data preprocessing...
Start to train weights...
100%|██████████| 4/4 [00:06<00:00,  1.67s/it]
Start to predict...
100%|██████████| 4/4 [00:02<00:00,  1.80it/s]
Show prediction results...
```

<img src="https://github.com/claudiiolima/ShapeRecognitionHopfield/blob/master/imgs/result.png" width=30%>

```bash
Show network weights matrix...
```

<img src="https://github.com/claudiiolima/ShapeRecognition/blob/master/img/tmp/weights.png" width=50%>

## PyPaint

Is an application for drawing.

### The Usage

For now run `PyPaint/example.py`

## The Idea

Is to make this two app, become one, the Hopfield Network would be on background of PyPaint only print your results.

### How it will Work?

The PyPaint will have a signal that call a slot, from time to time, that saves an image of drawing. That image will send to HN via thread execution that will have an answer to draw.

## Reference

- Amari, "Neural theory of association and concept-formation", SI. Biol. Cybernetics (1977) 26: 175. https://doi.org/10.1007/BF00365229
- D. Pebly, "PyQt Painting widget", PyQtPaint (2017): https://github.com/dpebly/pyqt-paint
- J. J. Hopfield, "Neural networks and physical systems with emergent collective computational abilities", Proceedings of the National Academy of Sciences of the USA, vol. 79 no. 8 pp. 2554–2558, April 1982.
