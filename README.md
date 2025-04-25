# eecs_203a
EECS 203A LEC A: DIGITAL IMAGE PROCG (17340)

```mermaid
graph TD
    subgraph Input Data
        I0[x(0) ... x(7)]
        I1[x(8) ... x(15)]
        I2[x(16) ... x(23)]
    end

    subgraph FFT Chip 1 (8-point)
        FFT1
    end

    subgraph FFT Chip 2 (8-point)
        FFT2
    end

    subgraph FFT Chip 3 (8-point)
        FFT3
    end

    subgraph Twiddle Factor Multiplication (Stage 1)
        T00[Multiply by W_24^(0*0) ... W_24^(7*0)]
        T10[Multiply by W_24^(0*1) ... W_24^(7*1)]
        T20[Multiply by W_24^(0*2) ... W_24^(7*2)]
    end

    subgraph 3-point DFT (Conceptual)
        DFT3_0
        DFT3_1
        DFT3_2
        DFT3_3
        DFT3_4
        DFT3_5
        DFT3_6
        DFT3_7
    end

    subgraph Twiddle Factor Multiplication (Stage 2)
        TW0[Multiply by W_24^(0*0) ... W_24^(2*0)]
        TW1[Multiply by W_24^(0*1) ... W_24^(2*1)]
        TW2[Multiply by W_24^(0*2) ... W_24^(2*2)]
        TW3[Multiply by W_24^(0*3) ... W_24^(2*3)]
        TW4[Multiply by W_24^(0*4) ... W_24^(2*4)]
        TW5[Multiply by W_24^(0*5) ... W_24^(2*5)]
        TW6[Multiply by W_24^(0*6) ... W_24^(2*6)]
        TW7[Multiply by W_24^(0*7) ... W_24^(2*7)]
    end

    subgraph Output Data
        O0[X(0) ... X(7)]
        O1[X(8) ... X(15)]
        O2[X(16) ... X(23)]
    end

    I0 --> FFT1
    I1 --> FFT2
    I2 --> FFT3

    FFT1 --> T00
    FFT2 --> T10
    FFT3 --> T20

    T00 -- s=0 --> DFT3_0
    T10 -- s=0 --> DFT3_0
    T20 -- s=0 --> DFT3_0

    T00 -- s=1 --> DFT3_1
    T10 -- s=1 --> DFT3_1
    T20 -- s=1 --> DFT3_1

    T00 -- s=2 --> DFT3_2
    T10 -- s=2 --> DFT3_2
    T20 -- s=2 --> DFT3_2

    T00 -- s=3 --> DFT3_3
    T10 -- s=3 --> DFT3_3
    T20 -- s=3 --> DFT3_3

    T00 -- s=4 --> DFT3_4
    T10 -- s=4 --> DFT3_4
    T20 -- s=4 --> DFT3_4

    T00 -- s=5 --> DFT3_5
    T10 -- s=5 --> DFT3_5
    T20 -- s=5 --> DFT3_5

    T00 -- s=6 --> DFT3_6
    T10 -- s=6 --> DFT3_6
    T20 -- s=6 --> DFT3_6

    T00 -- s=7 --> DFT3_7
    T10 -- s=7 --> DFT3_7
    T20 -- s=7 --> DFT3_7

    DFT3_0 -- q=0 --> TW0
    DFT3_0 -- q=1 --> TW1
    DFT3_0 -- q=2 --> TW2

    DFT3_1 -- q=0 --> TW0
    DFT3_1 -- q=1 --> TW1
    DFT3_1 -- q=2 --> TW2

    DFT3_2 -- q=0 --> TW3
    DFT3_2 -- q=1 --> TW4
    DFT3_2 -- q=2 --> TW5

    DFT3_3 -- q=0 --> TW3
    DFT3_3 -- q=1 --> TW4
    DFT3_3 -- q=2 --> TW5

    DFT3_4 -- q=0 --> TW6
    DFT3_4 -- q=1 --> TW7
    DFT3_4 -- q=2 --> TW0

    DFT3_5 -- q=0 --> TW6
    DFT3_5 -- q=1 --> TW7
    DFT3_5 -- q=2 --> TW1

    DFT3_6 -- q=0 --> TW3
    DFT3_6 -- q=1 --> TW4
    DFT3_6 -- q=2 --> TW5

    DFT3_7 -- q=0 --> TW6
    DFT3_7 -- q=1 --> TW7
    DFT3_7 -- q=2 --> TW2

    TW0 --> O0
    TW1 --> O1
    TW2 --> O2
    TW3 --> O3
    TW4 --> O4
    TW5 --> O5
    TW6 --> O6
    TW7 --> O7
```