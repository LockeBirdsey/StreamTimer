from random import random

import PySimpleGUI as sg
import main as st
import time


class GUI:
    def main(self):
        timer = st.StreamTimer()
        sg.theme('DarkAmber')  # Add a touch of color
        # All the stuff inside your window.
        layout = [[sg.Text(timer.get_current_time_as_string(), key="TEXTDISP")],
                  [sg.Text('Start At Time'), sg.InputText(key="TIME_ENTRY", enable_events=True)],
                  [sg.Button("Start"), sg.Button("Pause"), sg.Button("Reset"), sg.Button("Change Direction")],
                  [sg.Text("File to Load/Save From: "), sg.Input(key="TIME_FILE_LOC", enable_events=True),
                   sg.FileBrowse(key="TIME_FILE", enable_events=True)],
                  [sg.Checkbox("Export to File", key="EXPORTING", enable_events=True, default=False)]]

        # Create the Window
        window = sg.Window('Stream Timer', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            if timer.is_active():
                event, values = window.read(timeout=10)
                timer.tick()
            else:
                event, values = window.read()

            if event in (None, 'Cancel'):  # if user closes window or clicks cancel
                # quit
                break
            if event in (None, 'Start'):
                timer.start_timer()

            if event in (None, 'Pause'):
                timer.pause_timer()

            if event in (None, 'Reset'):
                timer.reset_timer()

            if event in (None, 'Change Direction'):
                timer.flip_direction()

            if event in (None, 'TIME_FILE_LOC'):
                timer.set_file(values["TIME_FILE_LOC"])

            if event in (None, "EXPORTING"):
                time.set_writing_to_file(values["EXPORTING"])

            window['TEXTDISP'].update(timer.get_current_time_as_string())

        window.close()


if __name__ == '__main__':
    gui = GUI()
    gui.main()
