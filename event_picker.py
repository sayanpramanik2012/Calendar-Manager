import json
import tkinter as tk


def update_checkbox_state(data, checkbox_vars, index):
    # Update the alert value based on checkbox state
    if checkbox_vars[index].get() == 1:
        data["dates"][index]["alert"] = "1"
    else:
        data["dates"][index]["alert"] = "0"


def create_checkbox(data, checkbox_vars, event_window, index):
    checkbox = tk.Checkbutton(
        event_window,
        variable=checkbox_vars[index],
        command=lambda: update_checkbox_state(data, checkbox_vars, index),
    )
    checkbox.grid(row=index + 1, column=1)


def create_label(date, event_window, index):
    label = tk.Label(event_window, text=date)
    label.grid(row=index + 1, column=0)


def done(data, event_window):
    # Update the JSON file with the modified data
    with open("assets/upcoming.json", "w") as file:
        json.dump(data, file, indent=2)
    event_window.destroy()


def create_event_window():
    # Read the JSON file
    with open("assets/upcoming.json") as file:
        data = json.load(file)

    event_window = tk.Tk()
    event_window.title("Event Window")

    checkbox_vars = []

    # Create checkboxes and labels dynamically
    for index, date_entry in enumerate(data["dates"]):
        date = date_entry["date"]
        alert = date_entry["alert"]

        checkbox_var = tk.IntVar(value=int(alert))
        checkbox_vars.append(checkbox_var)

        create_label(date, event_window, index)
        create_checkbox(data, checkbox_vars, event_window, index)

    done_button = tk.Button(
        event_window, text="Done", command=lambda: done(data, event_window)
    )
    done_button.grid(row=len(data["dates"]) + 1, column=0, columnspan=2)

    event_window.mainloop()
