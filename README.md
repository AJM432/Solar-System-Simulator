<div align="center">
<img src="https://user-images.githubusercontent.com/49791407/186054817-eafde350-7d1c-4bef-9ea4-9d9cf99cb190.png">
<b>Simulates the solar system using Newton's laws of gravitational motion.</b>
</div>

<br>

![](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=blue&color=white) 
![](https://img.shields.io/tokei/lines/github/AJM432/Solar-System-Simulator) 
![](https://img.shields.io/github/repo-size/AJM432/Solar-System-Simulator?style=flat)

## Demo
![Github Solar System](https://user-images.githubusercontent.com/49791407/165391132-9058ea45-daa2-44e1-a6b0-a1174996bfec.gif)

## Usage
- You may change the number of planets in the solar system by going to ![main.py](https://github.com/AJM432/Solar-System-Simulator/blob/main/main.py) and changing the value of the "solar_system" dictionary, which includes multiple instances of the CelestialBody class.

```py
solar_system = {
    'sun' : CelestialBody(name='sun', mass=200000, x=WIDTH//2, y=HEIGHT//2, vx=0, vy=0, color=PALE_YELLOW, radius=10, is_influenced=False),
    'mercury' : CelestialBody(name='mercury', mass=200, x=WIDTH//2-50, y=HEIGHT//2, vx=0, vy=6, color=WHITE, radius=3),
    'venus' : CelestialBody(name='venus', mass=200, x=WIDTH//2-100, y=HEIGHT//2, vx=0.5, vy= 3, color=PINK, radius=3),
    'earth' : CelestialBody(name='earth', mass=200, x=WIDTH//2-150, y=HEIGHT//2, vx=0, vy=-4, color=BLUE, radius=7),
    'mars' : CelestialBody(name='mars', mass=200, x=WIDTH//2-200, y=HEIGHT//2, vx=0, vy=5, color=RED, radius=5),
    'jupiter' : CelestialBody(name='jupiter', mass=200, x=WIDTH//2-300, y=HEIGHT//2, vx=0, vy=-3, color=RED, radius=15),
    'saturn' : CelestialBody(name='saturn', mass=200, x=WIDTH//2-400, y=HEIGHT//2, vx=0, vy=-2, color=PALE_YELLOW, radius=13),
    'uranus' : CelestialBody(name='uranus', mass=200, x=WIDTH//2-500, y=HEIGHT//2, vx=0, vy=-2, color=BLUE, radius=11),
    'neptune' : CelestialBody(name='neptune', mass=200, x=WIDTH//2-600, y=HEIGHT//2, vx=0, vy=-1, color=BLUE, radius=11)
    }
```

## License

Solar-System-Simulator is licensed under the ![MIT license](https://github.com/AJM432/Solar-System-Simulator/blob/main/LICENSE.md).
