import streamlit as st
import numpy as np
from typing import Any
#st.write("可以调用方法一")
# Interactive Streamlit elements, like these sliders, return their value.
# This gives you an extremely simple interaction model.

st.sidebar.write("_:blue[编队分形模拟运行]_")    
iterations = st.sidebar.slider("细节层次(LOD)", 2, 20, 10, 1)
separation = st.sidebar.slider("分形分离参数(Separation)", 0.7, 2.0, 0.7885)
st.caption("此动画展示了在纯无源情况下初始无人机在基于Julia集模拟运行的定位过程,可以通过左侧“细节层次(LOD)”与“分离参数”调控算法的运行过程")
# Non-interactive elements return a placeholder to their location
# in the app. Here we're storing progress_bar to update it later.
progress_bar = st.sidebar.progress(0)

# These two elements will be filled in later, so we create a placeholder
# for them using st.empty()
frame_text = st.sidebar.empty()
image = st.empty()

m, n, s = 960, 640, 400
x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))

for frame_num, a in enumerate(np.linspace(0.0, 4 * np.pi, 100)):
    # Here were setting value for these two elements.
    progress_bar.progress(frame_num)
    frame_text.text("任务加载进度 %i/100" % (frame_num + 1))

    # Performing some fractal wizardry.
    c = separation * np.exp(1j * a)
    Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    C = np.full((n, m), c)
    M: Any = np.full((n, m), True, dtype=bool)
    N = np.zeros((n, m))

    for i in range(iterations):
        Z[M] = Z[M] * Z[M] + C[M]
        M[np.abs(Z) > 2] = False
        N[M] = i

    # Update the image placeholder by calling the image() function on it.
    image.image(1.0 - (N / N.max()), use_column_width=True)

# We clear elements by calling empty on them.
progress_bar.empty()
frame_text.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("再次运行",key=1)