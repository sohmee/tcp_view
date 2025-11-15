import gi
import socket
import psutil
import random
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

class TcpView(Gtk.Window):
    def __init__(self):
        super().__init__(title="Linux TcpView")
        self.set_default_size(1000, 500)

        self.active_only = True
        self.show_tcp = True
        self.show_udp = True
        self.show_ipv4 = True
        self.show_ipv6 = True
        self.process_colors = {}

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        # CSS styling
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_data(b"""
            .active-button {
                background-color: #007BFF;
                color: white;
            }
        """)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Filter buttons
        self.filter_box = Gtk.Box(spacing=6)
        self.box.pack_start(self.filter_box, False, False, 0)

        self.active_toggle = self.make_toggle("Active Only", self.toggle_active)
        self.tcp_toggle = self.make_toggle("TCP", self.toggle_tcp)
        self.udp_toggle = self.make_toggle("UDP", self.toggle_udp)
        self.ipv4_toggle = self.make_toggle("IPv4", self.toggle_ipv4)
        self.ipv6_toggle = self.make_toggle("IPv6", self.toggle_ipv6)

        # Connection list with color column
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.liststore)

        self.columns = ["Proto", "IP Ver", "Local Address", "Remote Address", "Status", "Process"]
        for i, title in enumerate(self.columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i)
            column.set_sort_column_id(i)
            column.add_attribute(renderer, "cell-background", 6)  # Use color column
            self.treeview.append_column(column)

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.add(self.treeview)
        self.box.pack_start(self.scroll, True, True, 0)

        self.refresh_connections()
        GLib.timeout_add_seconds(5, self.refresh_connections)

    def make_toggle(self, label, callback):
        button = Gtk.ToggleButton(label=label)
        button.set_active(True)
        button.connect("toggled", callback)
        self.filter_box.pack_start(button, False, False, 0)
        self.update_button_style(button)
        return button

    def update_button_style(self, button):
        context = button.get_style_context()
        if button.get_active():
            context.add_class("active-button")
        else:
            context.remove_class("active-button")

    def toggle_active(self, widget):
        self.active_only = widget.get_active()
        self.update_button_style(widget)
        self.refresh_connections()

    def toggle_tcp(self, widget):
        self.show_tcp = widget.get_active()
        self.update_button_style(widget)
        self.refresh_connections()

    def toggle_udp(self, widget):
        self.show_udp = widget.get_active()
        self.update_button_style(widget)
        self.refresh_connections()

    def toggle_ipv4(self, widget):
        self.show_ipv4 = widget.get_active()
        self.update_button_style(widget)
        self.refresh_connections()

    def toggle_ipv6(self, widget):
        self.show_ipv6 = widget.get_active()
        self.update_button_style(widget)
        self.refresh_connections()

    def get_color_for_process(self, name):
        if name not in self.process_colors:
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            self.process_colors[name] = f"#{r:02x}{g:02x}{b:02x}"
        return self.process_colors[name]

    def refresh_connections(self):
        self.liststore.clear()
        for conn in psutil.net_connections(kind='inet6') + psutil.net_connections(kind='inet'):
            if self.active_only and conn.status != 'ESTABLISHED':
                continue
            proto = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            if proto == "TCP" and not self.show_tcp:
                continue
            if proto == "UDP" and not self.show_udp:
                continue
            ipver = "IPv6" if ':' in conn.laddr.ip else "IPv4"
            if ipver == "IPv4" and not self.show_ipv4:
                continue
            if ipver == "IPv6" and not self.show_ipv6:
                continue
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
            pid = conn.pid
            proc_name = ""
            if pid:
                try:
                    proc_name = psutil.Process(pid).name()
                except Exception:
                    proc_name = "?"
            color = self.get_color_for_process(proc_name)
            self.liststore.append([proto, ipver, laddr, raddr, conn.status, proc_name, color])
        return True

win = TcpView()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
