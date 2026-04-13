# SDN-Based Traffic Control and OpenFlow Rule Implementation using POX and Mininet

---

## 📌 Project Description

This project demonstrates a Software Defined Networking (SDN) environment using Mininet and the POX controller. The controller dynamically manages network traffic using OpenFlow-based match–action rules. It classifies packets based on protocol type (ICMP, TCP) and enforces traffic control policies, including allowing normal traffic and blocking specific hosts.

The project highlights how centralized control in SDN enables flexible and programmable network behavior.

---

## 🎯 Objectives

* Demonstrate controller–switch interaction
* Handle `packet_in` events in POX
* Implement OpenFlow match–action flow rules
* Classify network traffic (ICMP, TCP)
* Demonstrate allowed vs blocked traffic scenarios
* Analyze network performance using ping and iperf

---

## 🧠 Key Concepts

### 🔹 Software Defined Networking (SDN)

SDN separates:

* **Control Plane** → Controller (POX)
* **Data Plane** → Switch (Open vSwitch)

This allows centralized and programmable control of the network.

---

### 🔹 OpenFlow Protocol

OpenFlow is used for communication between controller and switch.

It works using:

* Flow tables inside switches
* Rules installed by controller
* Packet forwarding based on match–action logic

---

### 🔹 Match–Action Flow Rules

Each rule consists of:

**Match Fields:**

* IP packets (`dl_type=0x0800`)
* Protocol type (ICMP = 1, TCP = 6)
* Source IP address

**Actions:**

* Forward (FLOOD)
* Drop (Block traffic)

**Priority:**

* Determines rule importance

---

## 🏗️ Network Topology

* 1 Switch (s1)
* 3 Hosts:

  * h1 → 10.0.0.1
  * h2 → 10.0.0.2
  * h3 → 10.0.0.3

Topology:

```
h1 ─┐
     ├── s1 (OpenFlow Switch)
h2 ─┤
h3 ─┘
```

---

## 📁 Project Structure

```
project-folder/
│
├── qos_controller.py     # POX Controller logic
├── README.md             # Project documentation
├── screenshots/          # Output screenshots (optional)
│   ├── pox_running.png
│   ├── ping_results.png
│   ├── flow_table.png
│   └── blocked_traffic.png
```

---

## ⚙️ Requirements

* Ubuntu (VM or native)
* Mininet
* POX Controller
* Python 3
* iperf
* xterm

---

## 🛠️ Setup & Execution

### 1️⃣ Start POX Controller

```bash
cd pox
python3 pox.py log.level --DEBUG openflow.of_01 qos_controller
```

---

### 2️⃣ Start Mininet

```bash
sudo mn -c
sudo mn --topo single,3 --controller=remote,ip=127.0.0.1
```

---

### 3️⃣ Verify Connectivity

```bash
pingall
```

Expected:

```
0% dropped
```

---

## 🧪 Test Scenarios

---

### 🔹 Scenario 1: Normal Traffic (Allowed)

#### Commands:

```bash
h1 ping -c 3 h2
h2 ping -c 3 h3
h3 ping -c 3 h1
```

#### TCP Traffic:

```bash
h1 iperf -s
xterm h2
iperf -c 10.0.0.1
```

#### Expected Results:

* All hosts communicate successfully
* Controller logs:

  * ICMP → HIGH PRIORITY
  * TCP → MEDIUM PRIORITY

---

### 🔹 Scenario 2: Blocked Traffic (Failure Case)

Controller blocks traffic from **h1 (10.0.0.1)**

#### Command:

```bash
h1 ping h2
```

#### Expected Result:

* Ping fails ❌
* Other hosts communicate normally ✔️
* Controller log:

```
BLOCKED: h1 traffic dropped
```

---

## 📊 Flow Table Inspection

```bash
dpctl dump-flows
```

Example entries:

```
nw_proto=1 → ICMP
nw_proto=6 → TCP
priority=100
priority=50
```

---

## 📊 Performance Analysis

| Metric     | Tool  | Observation     |
| ---------- | ----- | --------------- |
| Latency    | ping  | Low delay       |
| Throughput | iperf | High bandwidth  |
| Flow Rules | dpctl | Dynamic updates |

---

## 💻 Controller Logic (Summary)

* Listens for `PacketIn` events
* Identifies packet type (ICMP/TCP)
* Applies traffic rules:

  * Allow → Forward
  * Block → Drop
* Installs OpenFlow rules dynamically

---

## 📸 Proof of Execution

Include screenshots of:

* POX controller running
* Mininet topology
* Ping results
* iperf output
* Flow table (`dpctl dump-flows`)
* Blocked traffic output

---

## ✅ Conclusion

This project successfully demonstrates SDN-based traffic management using POX and Mininet. It shows how OpenFlow rules can dynamically control network behavior, classify traffic, and enforce policies such as blocking specific hosts.

---

## 📚 References

* Mininet Documentation
* POX Controller Documentation
* OpenFlow Specification

---
