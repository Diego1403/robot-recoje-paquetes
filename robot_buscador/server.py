import paho.mqtt.client as mqtt
import tkinter as tk

broker_address = "192.168.48.245"
broker_port = 1883
topic_map = "map"
topic_map_send = "grupoN/send_package"
topic_map_recive = "grupoN/recive_package"

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
        # Row Entry
        self.row_label = tk.Label(self.entry_frame, text="Row:")
        self.row_label.grid(row=0, column=0, padx=5, pady=5)
        self.row_entry = tk.Entry(self.entry_frame, width=5)
        self.row_entry.grid(row=0, column=1, padx=5, pady=5)
        # Column Entry
        self.col_label = tk.Label(self.entry_frame, text="Column:")
        self.col_label.grid(row=1, column=0, padx=5, pady=5)
        self.col_entry = tk.Entry(self.entry_frame, width=5)
        self.col_entry.grid(row=1, column=1, padx=5, pady=5)

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
        client.subscribe(topic_map)
        
    def send_package(self):
        try:
            row = int(self.row_entry.get())
            col = int(self.col_entry.get())
            if row < 1 or row > 5 or col < 1 or col > 7:
                raise ValueError("Row or column out of range")
            self.coordinates.append((row, col))
            self.sent_coordinates.append((row, col))
            self.update_sent_coordinates_listbox()
            self.draw_coordinate(row, col)

            self.client.publish(topic_map_send, f"{row},{col}")
            print(f"Published coordinates: Row {row}, Column {col}")
        except ValueError:
            print("Invalid coordinate. Please enter integers between 1 and 5 for row and between 1 and 7 for column.")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        try:
            data = msg.payload.decode("utf-8") 
            row, col = map(int, data.split(',')) 
            self.draw_coordinate(row, col)
            
        except Exception as e:
            print("Error:", e)

    def draw_coordinate(self, row, col):
        x = (col - 1) * 50 + 25
        y = (row - 1) * 50 + 25
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red")
        
    def update_sent_coordinates_listbox(self):
        self.sent_coordinates_listbox.delete(0, tk.END)
        for coord in self.sent_coordinates:
            self.sent_coordinates_listbox.insert(tk.END, f"Row: {coord[0]}, Column: {coord[1]}")

def main():
    root = tk.Tk()
    app = PackageSender(root)
    root.mainloop()

if __name__ == "__main__":
    main()
