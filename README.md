# ESP32 CAN2BT OBD Dashboard
🚗 Project Overview | Proje Özeti
English:
This project enables real-time reading of OBD-II vehicle data via the CAN Bus using an ESP32 and MCP2515 module. The data is transmitted over Bluetooth and visualized on a custom dashboard. It is designed for educational and prototyping purposes.

Türkçe:
Bu proje, ESP32 ve MCP2515 modülü kullanarak OBD-II araç verilerini CAN Bus üzerinden gerçek zamanlı olarak okumayı sağlar. Okunan veriler Bluetooth üzerinden aktarılır ve özel bir dashboard üzerinde görselleştirilir. Eğitim ve prototipleme amacıyla geliştirilmiştir.

🛠️ Features | Özellikler
Real-time OBD-II data reading

CAN Bus communication (500 kbps)

Bluetooth data streaming via ESP32

Custom dashboard visualization

Sequential PID requests (RPM, Speed, Engine Load, Coolant Temp)

Gerçek zamanlı OBD-II veri okuma

CAN Bus haberleşmesi (500 kbps)

ESP32 üzerinden Bluetooth veri aktarımı

Özel dashboard görselleştirmesi

Sıralı PID sorguları (Devir, Hız, Motor Yükü, Soğutma Sıcaklığı)

🔧 Hardware Requirements | Donanım Gereksinimleri
ESP32

MCP2515 CAN Bus Module

OBD-II to CAN Adapter

Desktop or Laptop device (for Bluetooth display)

(Optional) External power supply for automotive testing

🔌 Connection Diagram | Bağlantı Şeması
![Ekran görüntüsü 2025-06-13 112831](https://github.com/user-attachments/assets/12696b13-2059-48a2-bb7e-933a3ecfa188)


📊 Dashboard Preview | Dashboard Görseli
![Ekran görüntüsü 2025-06-10 225511](https://github.com/user-attachments/assets/2af8cbb8-9853-4924-8671-9772e98a0ffe)


🚙 Supported OBD-II PIDs | Desteklenen OBD-II PID'leri
Engine RPM
Vehicle Speed
Engine Coolant Temperature
Engine Load

Motor Devir (RPM)
Araç Hızı
Motor Soğutma Sıcaklığı
Motor Yükü

⚙️ Installation | Kurulum
Clone the repository:

bash
Copy
Edit
git clone https://github.com/erhanbilir/ESP32-CAN2BT-OBD-Dashboard.git
Open the project with Arduino IDE.

Install the required libraries:

mcp2515

BluetoothSerial

Upload the code to the ESP32.

Connect hardware as shown in the connection diagram.

🚀 How to Use | Nasıl Kullanılır
Power the ESP32 and CAN module.

Connect OBD-II port to the MCP2515 via CAN adapter.

Pair your phone with the ESP32 via Bluetooth (OBD_BT by default).

Open the dashboard interface on your phone or PC.

Monitor vehicle data in real-time.

ESP32 ve CAN modülünü besleyin.

OBD-II portunu MCP2515’e bağlayın.

Telefonunuzu Bluetooth üzerinden ESP32 ile eşleştirin (OBD_BT varsayılan).

Telefon veya PC üzerinden dashboard arayüzünü açın.

Araç verilerini gerçek zamanlı olarak takip edin.
