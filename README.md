Apsera Digital Receiver Simulation

This repository contains Python code for simulating key blocks of a radio astronomy digital receiver chain,. The simulation closely models the constraints and modules of real FPGA-based digital backends—like those used in the Apsera telescope—including realistic handling of ADC, windowing, truncation, FFT, and correlation. It is intended as an accessible foundation for students, engineers, and researchers working on digital signal processing for radio astronomy and related applications.
Features

    Digital Signal Chain Modeling
    Simulates core stages: signal generation, ADC quantization, windowing, pipelined FFT, truncation, auto- and cross-correlation, and accumulation.

    Hardware-Accurate Constraints
    Reflects word-lengths, bit growth, and architectural limits of actual FPGAs (Red Pitaya-class), ensuring code results are relevant for rapid prototyping and real-world deployment.

    Modular Python Workflow
    Each processing stage is separated for transparency and ease of experimentation. Input signals, window types, and other parameters are easily configurable.

    Visualization and Analysis
    Built-in plotting shows spectra, time/data accuracies, and processing trade-offs at each stage for clear interpretation of signal quality and hardware impact.

    Educational Value
    Code, comments, and workflow reflect best practices in signal processing, making this a useful entry point for FPGA–DSP co-design or for classroom/lab projects.

This code is based on work for the Apsera digital backend simulation, as detailed in the project report https://docs.google.com/document/d/1QcGJdBPNrxv6g5BNHXj0NK9xeyR1mIa82bK2W6tLLVw/edit?tab=t.0#heading=h.gudloz4isnjq.
Key concepts and implementation decisions closely follow practical constraints of radio telescope instrument design, especially those using FPGAs for high-speed DSP.
    
