
import sys
import time
import math
import serial
import serial.tools.list_ports
import threading
from PyQt5.QtCore import Qt, QRectF, QTimer, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QRadialGradient, QLinearGradient, QPainterPath, QFontDatabase
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

class ModernDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Dashboard V2")
        self.resize(1200, 600)

        # Indicator values (just for initialization, will be updated from serial data later)
        self.speed = 0
        self.rpm = 0
        self.load = 0
        self.temp = 0

        # Digital clock
        self.time = time.localtime()

        # Animation values
        self.startup_animation = 0
        self.needle_vibration = 0
        self.alert_blink = 0

        # Indicator colors
        self.theme_color = QColor(30, 170, 230)
        self.warning_color = QColor(255, 160, 0)
        self.danger_color = QColor(255, 60, 60)
        self.normal_color = QColor(80, 220, 170)

        # Special Font Loading
        QFontDatabase.addApplicationFont(":/fonts/digital.ttf")

        # Serial port interface
        self.combobox_port = QComboBox(self)
        self.combobox_baud = QComboBox(self)
        self.button_connect = QPushButton("Connect", self)
        self.label_status = QLabel("Not Connected", self)

        self.combobox_baud.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.refreshSerialPorts()
        self.button_connect.clicked.connect(self.toggleSerialConnection)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.combobox_port)
        layout.addWidget(QLabel("Baud:"))
        layout.addWidget(self.combobox_baud)
        layout.addWidget(self.button_connect)
        layout.addWidget(self.label_status)

        vlayout = QVBoxLayout(self)
        vlayout.addLayout(layout)
        vlayout.addStretch()
        self.setLayout(vlayout)

        # Serial port transactions
        self.serial_port = None
        self.serial_thread = None
        self.serial_running = False

        # Indicator update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.updateValues)
        self.update_timer.start(16)

        # Beginning animation
        self.startup_timer = QTimer()
        self.startup_timer.timeout.connect(self.updateStartupAnimation)
        self.startup_timer.start(40)

        # Message system
        self.current_message = ""

    def refreshSerialPorts(self):
        self.combobox_port.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.combobox_port.addItem(port.device)

    def toggleSerialConnection(self):
        if self.serial_running:
            self.serial_running = False
            if self.serial_port:
                self.serial_port.close()
            self.button_connect.setText("Connect")
            self.label_status.setText("Not Connected")
        else:
            port = self.combobox_port.currentText()
            baud = int(self.combobox_baud.currentText())
            try:
                self.serial_port = serial.Serial(port, baud, timeout=1)
                self.serial_running = True
                self.button_connect.setText("Disconnect")
                self.label_status.setText(f"{port} @ {baud}")
                self.serial_thread = threading.Thread(target=self.readSerialData, daemon=True)
                self.serial_thread.start()
            except Exception as e:
                self.label_status.setText(f"Error: {e}")

    def readSerialData(self):
        while self.serial_running and self.serial_port and self.serial_port.is_open:
            try:
                line = self.serial_port.readline().decode(errors='ignore').strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 4:
                        speed, rpm, load, temp = parts
                        self.speed = float(speed)
                        self.rpm = float(rpm)
                        self.load = float(load)
                        self.temp = float(temp)
            except Exception:
                pass

    def updateStartupAnimation(self):
        if self.startup_animation < 100:
            self.startup_animation += 2
            self.update()
        else:
            self.startup_timer.stop()

    def updateValues(self):
        # Vibration effect and warning effect
        self.needle_vibration = math.sin(time.time() * 20) * (0.5 + self.rpm / 16000)
        self.alert_blink = (math.sin(time.time() * 8) + 1) / 2
        self.time = time.localtime()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        bg_gradient = QLinearGradient(0, 0, self.width(), self.height())
        bg_gradient.setColorAt(0, QColor(25, 30, 40))
        bg_gradient.setColorAt(1, QColor(15, 20, 30))
        painter.fillRect(self.rect(), bg_gradient)

        # Animation effect - boot screen
        if self.startup_animation < 100:
            painter.setOpacity(self.startup_animation / 100)
        else:
            painter.setOpacity(1.0)

        gauge_radius = min(self.width(), self.height()) / 6

        # RMP indicator (left top)
        rpm_center = QPointF(self.width() * 0.25, self.height() * 0.33)
        self.drawModernGauge(
            painter, rpm_center, gauge_radius * 1.1,
            0, 8000, self.rpm, "RPM"
        )

        # Analog speedometer (right top)
        speed_center = QPointF(self.width() * 0.75, self.height() * 0.33)
        self.drawModernGauge(
            painter, speed_center, gauge_radius * 1.1,
            0, 240, self.speed, "SPEED",
            color_scheme="blue"
        )

        # Digital speedometer (center)
        digital_speed_rect = QRectF(
            self.width() / 2 - gauge_radius * 0.8,
            self.height() * 0.40,
            gauge_radius * 1.6,
            gauge_radius * 0.7
        )
        self.drawDigitalSpeed(painter, digital_speed_rect)

        # Engine temperature indicator (middle bottom)
        temp_center = QPointF(self.width() * 0.2, self.height() * 0.75)
        self.drawModernGauge(
            painter, temp_center, gauge_radius * 0.75,
            0, 130, self.temp, "TEMPERATURE",
            color_scheme="yellow"
        )

        # Engine load indicator (middle bottom)
        load_center = QPointF(self.width() * 0.8, self.height() * 0.75)
        self.drawModernGauge(
            painter, load_center, gauge_radius * 0.75,
            0, 100, self.load, "LOAD",
            color_scheme="green"
        )

        # Clock (Right top)
        clock_rect = QRectF(
            self.width() - 100, 20,
            80, 25
        )
        self.drawDigitalClock(painter, clock_rect)

        # Control instructions
        if self.startup_animation >= 100:
            controls_text = "Waiting for data from serial port..."
            painter.setFont(QFont("Arial", 8))
            painter.setPen(QColor(120, 125, 135))
            painter.drawText(10, self.height() - 10, controls_text)

    def drawDigitalSpeed(self, painter, rect):
        bg_path = QPainterPath()
        bg_path.addRoundedRect(rect, 15, 15)
        bg_gradient = QLinearGradient(rect.topLeft(), rect.bottomRight())
        bg_gradient.setColorAt(0, QColor(25, 27, 40))
        bg_gradient.setColorAt(1, QColor(35, 40, 55))
        painter.setPen(QPen(QColor(60, 70, 80), 1))
        painter.setBrush(bg_gradient)
        painter.drawPath(bg_path)
        highlight = QLinearGradient(
            rect.x(), rect.y(),
            rect.x(), rect.y() + rect.height() * 0.5
        )
        highlight.setColorAt(0, QColor(255, 255, 255, 30))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(highlight)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(
            int(rect.x() + 2), int(rect.y() + 2),
            int(rect.width() - 4), int(rect.height() * 0.4),
            10, 10
        )
        speed_str = f"{int(self.speed)}"
        if self.speed > 180:
            speed_color = self.danger_color
        elif self.speed > 120:
            speed_color = self.warning_color
        else:
            speed_color = self.theme_color
        painter.setFont(QFont("Digital-7", 50, QFont.Bold))
        painter.setPen(QPen(QColor(0, 0, 0, 120)))
        painter.drawText(rect.adjusted(3, 3, 3, 3), Qt.AlignCenter, speed_str)
        painter.setPen(QPen(speed_color))

        painter.drawText(rect, Qt.AlignCenter, speed_str)
        painter.setFont(QFont("Arial", 14))
        painter.setPen(QPen(QColor(200, 200, 230)))
        km_rect = QRectF(rect.x(), rect.y() + rect.height() / 2 + 15, rect.width(), 20)
        painter.drawText(km_rect, Qt.AlignCenter, "km/h")
        glow_pen = QPen(speed_color)
        glow_pen.setWidth(2)
        painter.setPen(glow_pen)
        painter.setBrush(Qt.NoBrush)
        top_line_rect = QRectF(rect.x() + 15, rect.y() + 10, rect.width() - 30, 2)
        painter.drawLine(top_line_rect.topLeft(), top_line_rect.topRight())

    def drawModernGauge(self, painter, center, radius, min_val, max_val, value, label,
                        start_angle=225, sweep_angle=270, color_scheme="blue"):
        
        if color_scheme == "red":
            main_color = self.danger_color
        elif color_scheme == "yellow":
            main_color = self.warning_color
        elif color_scheme == "green":
            main_color = self.normal_color
        else:
            main_color = self.theme_color

        # Multiple ring effect
        for i in range(3):
            painter.setPen(QPen(QColor(60 + i*20, 60 + i*20, 70 + i*20, 150 - i*40), 1))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(center, radius - i*4, radius - i*4)

        # Background gradient
        bg_gradient = QRadialGradient(center, radius)
        bg_gradient.setColorAt(0, QColor(40, 45, 55))
        bg_gradient.setColorAt(0.97, QColor(30, 35, 45))
        bg_gradient.setColorAt(1, QColor(20, 25, 35))
        painter.setBrush(bg_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center, radius - 1, radius - 1)

        # Tick marks and numbers
        painter.setPen(QPen(QColor(120, 130, 140), 1.5))
        num_ticks = 11
        for i in range(num_ticks):
            ratio = i / (num_ticks - 1)
            angle_deg = start_angle - ratio * sweep_angle
            angle_rad = math.radians(angle_deg)
            outer_radius = radius - 2
            inner_radius = radius - 12
            
            if i % 5 == 0:
                inner_radius = radius - 20
                painter.setPen(QPen(QColor(180, 190, 200), 2))
            else:
                painter.setPen(QPen(QColor(120, 130, 140), 1))
            
            outer = QPointF(center.x() + math.cos(angle_rad) * outer_radius,
                            center.y() + math.sin(angle_rad) * outer_radius)
            inner = QPointF(center.x() + math.cos(angle_rad) * inner_radius,
                            center.y() + math.sin(angle_rad) * inner_radius)
            painter.drawLine(inner, outer)
            
            # Sayılar
            if i % 5 == 0:
                tick_value = min_val + ratio * (max_val - min_val)
                text_radius = radius - 35
                value_text = f"{int(tick_value)}"
                text_point = QPointF(
                    center.x() + math.cos(angle_rad) * text_radius,
                    center.y() + math.sin(angle_rad) * text_radius
                )
                painter.setFont(QFont("Arial", 8))
                painter.setPen(QPen(QColor(160, 170, 180)))
                text_rect = QRectF(
                    text_point.x() - 15, text_point.y() - 8,
                    30, 16
                )
                painter.drawText(text_rect, Qt.AlignCenter, value_text)

        # Bow drawing (progress arc)
        arc_rect = QRectF(
            center.x() - radius + 15,
            center.y() - radius + 15,
            2 * (radius - 15),
            2 * (radius - 15)
        )
        
        qt_start_angle = 135
        qt_sweep_angle = 270
        value_ratio = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        arc_span = value_ratio * qt_sweep_angle

        # Bow drawing
        painter.setPen(QPen(main_color, 4))
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(
            arc_rect,
            int(qt_start_angle * 16),
            int(arc_span * 16)
        )

        # Pointer drawing
        value_ratio = max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))
        qt_needle_angle = -qt_start_angle - value_ratio * qt_sweep_angle
        math_needle_angle = qt_needle_angle
        rad = math.radians(math_needle_angle)
        needle_length = radius - 25
        
        # Vibration effect
        vibration = self.needle_vibration * (0.5 + value / max_val) if label in ["DEVİR", "HIZ"] else 0
        vibration_rad = math.radians(vibration)
        rad += vibration_rad
        
        painter.setPen(QPen(main_color, 3.0, Qt.SolidLine, Qt.RoundCap))
        pt1 = QPointF(center.x(), center.y())
        pt2 = QPointF(
            center.x() + math.cos(rad) * needle_length,
            center.y() + math.sin(rad) * needle_length
        )
        painter.drawLine(pt1, pt2)
        
        # Center point
        center_gradient = QRadialGradient(
            center.x() - 2, center.y() - 2, 10
        )
        center_gradient.setColorAt(0, QColor(220, 220, 220))
        center_gradient.setColorAt(1, QColor(80, 80, 90))
        painter.setBrush(center_gradient)
        painter.setPen(QPen(QColor(40, 40, 50), 1))
        painter.drawEllipse(center, 6, 6)
        
        # Centeral highlight
        painter.setPen(Qt.NoPen)
        highlight_gradient = QRadialGradient(center, 3)
        highlight_gradient.setColorAt(0, QColor(255, 255, 255, 180))
        highlight_gradient.setColorAt(1, QColor(200, 200, 200, 0))
        painter.setBrush(highlight_gradient)
        painter.drawEllipse(center, 3, 3)
        
        # Value text
        if label == "RPM":
            value_text = f"{int(value)}"
        elif label == "TEMPERATURE":
            value_text = f"{int(value)}°C"
        elif label == "LOAD":
            value_text = f"{value:.1f}%"
        elif label == "SPEED":
            value_text = f"{int(value)}"
        else:
            value_text = f"{int(value)}"
        
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.setPen(main_color)
        value_rect = QRectF(
            center.x() - 40, center.y() + 10,
            80, 20
        )
        painter.drawText(value_rect, Qt.AlignCenter, value_text)
        
        # Label
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.setPen(QColor(170, 175, 180))
        label_rect = QRectF(
            center.x() - 40, center.y() + 30,
            80, 20
        )
        painter.drawText(label_rect, Qt.AlignCenter, label)

    def drawDigitalClock(self, painter, rect):
        hour = self.time.tm_hour
        minute = self.time.tm_min
        time_str = f"{hour:02d}:{minute:02d}"
        painter.setPen(QPen(QColor(60, 70, 80), 1))
        painter.setBrush(QColor(30, 35, 45))
        painter.drawRoundedRect(rect.toRect(), 5, 5)
        painter.setFont(QFont("Arial", 10))
        painter.setPen(QPen(QColor(180, 190, 200)))
        painter.drawText(rect, Qt.AlignCenter, time_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = ModernDashboard()
    dashboard.show()
    sys.exit(app.exec_())