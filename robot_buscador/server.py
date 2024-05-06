import paho.mqtt.client as mqtt
import tkinter as tk

broker_address = "192.168.48.245"
broker_port = 1883
topic_map = "map"
topic_map_send = "A3-467/grupoN/send_package"

class PackageSender:
    def __init__(self, master):
        self.master = master
        self.master.title("Package Sender")
        self.canvas = tk.Canvas(master, width=350, height=250)
        self.canvas.pack()
        self.coordinates = []
        self.sent_coordinates = []
        self.entry_frame = tk.Frame(master)
        self.entry_frame.pack()

        # Pickup Row Entry
        self.pickup_row_label = tk.Label(self.entry_frame, text="Pickup Row:")
        self.pickup_row_label.grid(row=0, column=2, padx=5, pady=5)
        self.pickup_row_entry = tk.Entry(self.entry_frame, width=5)
        self.pickup_row_entry.grid(row=0, column=3, padx=5, pady=5)
        # Pickup Column Entry
        self.pickup_col_label = tk.Label(self.entry_frame, text="Pickup Column:")
        self.pickup_col_label.grid(row=1, column=2, padx=5, pady=5)
        self.pickup_col_entry = tk.Entry(self.entry_frame, width=5)
        self.pickup_col_entry.grid(row=1, column=3, padx=5, pady=5)

        # Delivery Row Entry
        self.delivery_row_label = tk.Label(self.entry_frame, text="Delivery Row:")
        self.delivery_row_label.grid(row=2, column=2, padx=5, pady=5)
        self.delivery_row_entry = tk.Entry(self.entry_frame, width=5)
        self.delivery_row_entry.grid(row=2, column=3, padx=5, pady=5)
        # Delivery Column Entry
        self.delivery_col_label = tk.Label(self.entry_frame, text="Delivery Column:")
        self.delivery_col_label.grid(row=3, column=2, padx=5, pady=5)
        self.delivery_col_entry = tk.Entry(self.entry_frame, width=5)
        self.delivery_col_entry.grid(row=3, column=3, padx=5, pady=5)

        self.send_button = tk.Button(master, text="Send", command=self.send_package)
        self.send_button.pack(pady=5)
        self.sent_coordinates_listbox = tk.Listbox(master, height=10)
        self.sent_coordinates_listbox.pack(pady=5)

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, broker_port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(topic_map_send)
        
    def send_package(self):
        try:
            pickup_row = int(self.pickup_row_entry.get())
            pickup_col = int(self.pickup_col_entry.get())
            delivery_row = int(self.delivery_row_entry.get())
            delivery_col = int(self.delivery_col_entry.get())
            if (
                pickup_row < 1 or pickup_row > 5 or pickup_col < 1 or pickup_col > 7 or
                delivery_row < 1 or delivery_row > 5 or delivery_col < 1 or delivery_col > 7
            ):
                raise ValueError("Row or column out of range")
            self.coordinates.append((pickup_row, pickup_col))
            self.coordinates.append((delivery_row, delivery_col))
            self.sent_coordinates.append((pickup_row, pickup_col))
            self.sent_coordinates.append((delivery_row, delivery_col))
            self.update_sent_coordinates_listbox()
            self.draw_coordinate(pickup_row, pickup_col)
            self.draw_coordinate(delivery_row, delivery_col)
            self.pickup_row_entry.delete(0, tk.END)
            self.pickup_col_entry.delete(0, tk.END)
            self.delivery_row_entry.delete(0, tk.END)
            self.delivery_col_entry.delete(0, tk.END)
            
            payload = f"{pickup_row},{pickup_col};{delivery_row},{delivery_col}"
            self.client.publish(topic_map_send, payload)
        except ValueError as e:
            tk.messagebox.showerror("Error", str(e))
            try:
                pickup_row = int(self.pickup_row_entry.get())
                pickup_col = int(self.pickup_col_entry.get())
                delivery_row = int(self.delivery_row_entry.get())
                delivery_col = int(self.delivery_col_entry.get())
                if (
                    pickup_row < 1 or pickup_row > 5 or pickup_col < 1 or pickup_col > 7 or
                    delivery_row < 1 or delivery_row > 5 or delivery_col < 1 or delivery_col > 7
                ):
                    raise ValueError("Row or column out of range")
                self.coordinates.append((pickup_row, pickup_col))
                self.coordinates.append((delivery_row, delivery_col))
                self.sent_coordinates.append((pickup_row, pickup_col))
                self.sent_coordinates.append((delivery_row, delivery_col))
                self.update_sent_coordinates_listbox()
                self.draw_coordinate(pickup_row, pickup_col)
                self.draw_coordinate(delivery_row, delivery_col)
                self.row_entry.delete(0, tk.END)
                self.col_entry.delete(0, tk.END)
                self.pickup_row_entry.delete(0, tk.END)
                self.pickup_col_entry.delete(0, tk.END)
                self.delivery_row_entry.delete(0, tk.END)
                self.delivery_col_entry.delete(0, tk.END)
                
                payload = f"{pickup_row},{pickup_col};{delivery_row},{delivery_col}"
                self.client.publish(topic_map_send, payload)
            except ValueError as e:
                tk.messagebox.showerror("Error", str(e))
                
    def on_message(self, client, userdata, msg):
        message = msg.payload.decode("utf-8")
        print("Received message: " + message)
        coordinates = message.split(";")
        print(coordinates)
        for coord in coordinates:
            row, col = coord.split(",")
            self.draw_coordinate(int(row), int(col))
            
    def draw_coordinate(self, row, col):
        x = (col - 1) * 50
        y = (row - 1) * 50
        self.canvas.create_oval(x, y, x + 40, y + 40, fill="red")
        
    def update_sent_coordinates_listbox(self):
        self.sent_coordinates_listbox.delete(0, tk.END)
        for coord in self.sent_coordinates:
            self.sent_coordinates_listbox.insert(tk.END, f"Row: {coord[0]}, Col: {coord[1]}")

            
root = tk.Tk()
sender = PackageSender(root)
root.mainloop()
