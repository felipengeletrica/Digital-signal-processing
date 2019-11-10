from enum import Enum
from dsp_lab import *


class Process(Enum):
    DSP_OPEN_FILE = 0
    DSP_SAVE_FILE = 1
    DSP_PLOT_TIME_DOMAIN = 2
    DSP_PLOT_FREQUENCY_DOMAIN = 3
    DSP_FILTER = 4


def banner():
    print("-----------------------------------------")
    print("Welcome Digital Signal Processing Lab")
    print("Universidade Luterana do Brasil  2019/2")
    print('')
    print("Professor: Paulo Godoy")
    print("Alunos: Felipe Vargas e Tairon Coelho")
    print("-----------------------------------------")
    print("This Project remove interferente signal")
    print("-----------------------------------------")


def show_process_menu() -> Process:

    print('\n\r')
    for op in Process:
        print(f'{op.value} - {op.name}.')

    print('Q - EXIT.')
    option = input('Option:')
    if option is 'Q' or option is 'q':
        print("Bye Bye! :)")
        exit(0)
    return Process(int(option))


def show_filter_type() -> filter_type:

    print('\n\r')
    for op in filter_type:
        print(f'{op.value} - {op.name}.')

    print('Q - EXIT.')
    option = input('Option:')
    if option is 'Q' or option is 'q':
        return None
    return filter_type(int(option))


def file():

    print("Enter file name:")
    option = input()
    return option


def main():

    # Create instance for dsp lab
    dsp = dsp_lab()

    # Show main menu
    banner()
    while True:

        try:
            # Show menu
            opt = show_process_menu()

            # Open file
            if opt is Process.DSP_OPEN_FILE:
                print('Open file')
                filename = input('Filename:')
                audio_samples, sample_rate, duration = dsp.open(filename=filename)

                if audio_samples is not None:
                    print(f'Audio Number Samples: {len(audio_samples)}')
                    print(f'Sample Rate: {sample_rate}')
                    print(f'Duration: {duration}s')
                else:
                    print('Fail open file')

            # Save file
            elif opt is Process.DSP_SAVE_FILE:
                print('Save file')
                if len(dsp.audio_samples):
                    filename = input('Filename:')
                    dsp.save(filename=filename, audio_samples=dsp.audio_samples)

                else:
                    print('Not samples for save')

            # Plot audio time domain
            elif opt is Process.DSP_PLOT_TIME_DOMAIN:
                print("Print Frequency Domain")
                dsp.time_domain(audio_samples)

            elif opt is Process.DSP_PLOT_FREQUENCY_DOMAIN:
                print('Print Fast Transform Fourier (FFT)')
                dsp.frequency_domain(audio_samples)

            # Process audio filters
            elif opt is Process.DSP_FILTER:
                print("Processing filter...")
                option = show_filter_type()

                filtred_audio = dsp.filter(option)
                print('Save file')
                if len(filtred_audio):
                    filename = input('Filename:')
                    dsp.save(filename=filename, audio_samples=filtred_audio)
                    dsp.time_domain(filtred_audio)
                    dsp.frequency_domain(filtred_audio)



        except Exception as e:
            raise e


if __name__ == '__main__':
    main()