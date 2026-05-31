import ctypes, struct, math, wave, os, tempfile

sr = 44100
duration = 0.3
freq = 880
frames = int(sr * duration)
data = b"".join(
    struct.pack("<h", int(0.3 * 32767 * math.sin(2 * math.pi * freq * i / sr)))
    for i in range(frames)
)
path = os.path.join(tempfile.gettempdir(), "_diag_beep.wav")
with wave.open(path, "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(data)

mci = ctypes.windll.winmm.mciSendStringW
r1 = mci(f'open "{path}" alias diag_beep', None, 0, 0)
print(f"open: {r1}")
r2 = mci("play diag_beep wait", None, 0, 0)
print(f"play: {r2}")
mci("close diag_beep", None, 0, 0)
os.unlink(path)
print("BEEP OK")
