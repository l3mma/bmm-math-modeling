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
paraview_proc = None
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

def on_visualize_click():
    global paraview_proc
    paraview_exe = filedialog.askopenfilename(
        title="Выберите путь до ParaView.exe",
        filetypes=[("ParaView Executable", "*.exe")]
    )
    if not paraview_exe:
        return

    vtk_path = os.path.join(os.getcwd(), "output", "model.vtk")
    if not os.path.exists(vtk_path):
        messagebox.showerror("Ошибка", "VTK-файл не найден. Сначала сохраните его.")
        return

    kill_process(paraview_proc)
    paraview_proc = subprocess.Popen([paraview_exe, vtk_path])
    threading.Thread(target=lambda: (time.sleep(2), bring_window_to_front(paraview_proc.pid)), daemon=True).start()


# === Интерфейс ===

root = tk.Tk()
root.title("CAD Workflow")
root.state("zoomed")
root.configure(bg="white")

top_frame = tk.Frame(root, bg="white")
top_frame.pack(side="top", anchor="nw", fill="x")

button_style = {"font": ("Arial", 11), "bg": "#e0e0e0", "padx": 10, "pady": 6}

# === Панель кнопок ===

button_row = tk.Frame(top_frame, bg="white")
button_row.pack(side="top", padx=10, pady=10)

tk.Button(button_row, text="Import (Gmsh)", command=on_import_click, **button_style).pack(side="left", padx=5)
tk.Button(button_row, text="Сохранить как VTK", command=on_save_vtk_click, bg="#d0ffd0", font=("Arial", 11)).pack(side="left", padx=5)
tk.Button(button_row, text="Визуализировать", command=on_visualize_click, bg="#ffe0b3", font=("Arial", 11)).pack(side="left", padx=5)

workspace = tk.Frame(root, bg="#f8f8f8")
workspace.pack(fill="both", expand=True)

root.mainloop()
