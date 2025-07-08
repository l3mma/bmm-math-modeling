import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import time
import threading
import win32gui
import win32process
import win32con

# === Глобальные переменные ===
gmsh_proc = None
freecad_proc = None
gmsh_exe_path = None
last_cad_file = None

# === Вспомогательные функции ===

def bring_window_to_front(pid):
    def enum_windows(hwnd, _):
        _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
        if found_pid == pid and win32gui.IsWindowVisible(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.BringWindowToTop(hwnd)
    win32gui.EnumWindows(enum_windows, None)

def kill_process(proc):
    try:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
    except Exception:
        pass

# === Кнопки ===

def on_import_click():
    global gmsh_proc, gmsh_exe_path, last_cad_file
    cad_file = filedialog.askopenfilename(
        title="Выберите CAD файл",
        filetypes=[("CAD файлы", "*.step *.stp *.iges *.igs *.x_t *.x_b *.sat *.sab")]
    )
    if not cad_file:
        return

    gmsh_exe = filedialog.askopenfilename(
        title="Выберите путь до Gmsh.exe",
        filetypes=[("Gmsh Executable", "*.exe")]
    )
    if not gmsh_exe:
        return

    last_cad_file = cad_file
    gmsh_exe_path = gmsh_exe

    kill_process(gmsh_proc)
    gmsh_proc = subprocess.Popen([gmsh_exe_path, last_cad_file])
    threading.Thread(target=lambda: (time.sleep(2), bring_window_to_front(gmsh_proc.pid)), daemon=True).start()

def on_save_vtk_click():
    global gmsh_proc, last_cad_file, gmsh_exe_path
    if not last_cad_file or not gmsh_exe_path:
        messagebox.showerror("Ошибка", "Сначала импортируйте модель в Gmsh.")
        return

    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "model.vtk")

    try:
        subprocess.run([
            gmsh_exe_path,
            last_cad_file,
            "-3",
            "-format", "vtk",
            "-o", output_file
        ], check=True)
        messagebox.showinfo("Успех", f"VTK сохранён в: {output_file}")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", str(e))
        return

    kill_process(gmsh_proc)

def on_make_click():
    global freecad_proc
    freecad_exe = filedialog.askopenfilename(
        title="Выберите путь до FreeCAD.exe",
        filetypes=[("FreeCAD Executable", "*.exe")]
    )
    if not freecad_exe:
        return

    kill_process(freecad_proc)
    freecad_proc = subprocess.Popen([freecad_exe])
    threading.Thread(target=lambda: (time.sleep(2), bring_window_to_front(freecad_proc.pid)), daemon=True).start()

def on_export_iges_click():
    global freecad_proc
    fcstd_file = filedialog.askopenfilename(
        title="Выберите .FCStd файл (FreeCAD)",
        filetypes=[("FreeCAD Document", "*.FCStd")]
    )
    if not fcstd_file:
        return

    freecad_cmd = filedialog.askopenfilename(
        title="Выберите FreeCADCmd.exe",
        filetypes=[("FreeCADCmd Executable", "*.exe")]
    )
    if not freecad_cmd:
        return

    save_path = filedialog.asksaveasfilename(
        title="Сохранить как IGES",
        defaultextension=".iges",
        filetypes=[("IGES files", "*.iges")]
    )
    if not save_path:
        return

    script_path = os.path.join(os.getcwd(), "export_iges_temp.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"""
import FreeCAD
import ImportGui
doc = FreeCAD.open("{fcstd_file.replace("\\\\", "/")}")
objects = [obj for obj in doc.Objects if hasattr(obj, "Shape")]
ImportGui.export(objects, "{save_path.replace("\\\\", "/")}")
""")
    try:
        subprocess.run([freecad_cmd, script_path], check=True)
        messagebox.showinfo("Успех", f"IGES сохранён:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Ошибка экспорта", str(e))
    finally:
        if os.path.exists(script_path):
            os.remove(script_path)

    kill_process(freecad_proc)

# === Интерфейс ===

root = tk.Tk()
root.title("CAD Workflow")
root.state("zoomed")
root.configure(bg="white")

top_frame = tk.Frame(root, bg="white")
top_frame.pack(side="top", anchor="nw", fill="x")

button_style = {"font": ("Arial", 11), "bg": "#e0e0e0", "padx": 10, "pady": 6}

# Левая часть с кнопками Import + Сохранить VTK
left_buttons_frame = tk.Frame(top_frame, bg="white")
left_buttons_frame.pack(side="left", padx=10, pady=10)

tk.Button(left_buttons_frame, text="Import (Gmsh)", command=on_import_click, **button_style).pack(side="top", pady=5)
tk.Button(left_buttons_frame, text="Сохранить как VTK", command=on_save_vtk_click, bg="#d0ffd0", font=("Arial", 11)).pack(side="top", pady=5)

# Левая часть с кнопками Make + Сохранить CAD (IGES)
right_buttons_frame = tk.Frame(top_frame, bg="white")
right_buttons_frame.pack(side="left", padx=40, pady=10)

tk.Button(right_buttons_frame, text="Make in FreeCAD", command=on_make_click, **button_style).pack(side="top", pady=5)
tk.Button(right_buttons_frame, text="Сохранить CAD (IGES)", command=on_export_iges_click, bg="#d0e0ff", font=("Arial", 11)).pack(side="top", pady=5)

workspace = tk.Frame(root, bg="#f8f8f8")
workspace.pack(fill="both", expand=True)

root.mainloop()