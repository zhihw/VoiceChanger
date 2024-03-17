import voice_changer as vc




zone = {
    'Voice data processing': {
        'Record': '1',
        'Import': '2'
    },
    'Sound processing and playback': {
        'Original': '3',
        'Gender Transformation': '4',
        'Robot': '5',
        'Child Voice': '6'
    }
}

first_list = list(zone.keys())
original_data = None
while True:
    print("Welcome to the main menu")

    for i in first_list:
        print(first_list.index(i) + 1, i)
    
    choice1 = input("Please select the option number: [Enter q to exit]: ")
    
    if choice1.isdigit():
        choice1 = int(choice1)

        if 0 < choice1 <= len(first_list):
            first_name = first_list[choice1 - 1]
            second_list = list(zone[first_name])

            while True:
                for item in second_list:
                    print(second_list.index(item) + 1, item)
                
                choice2 = input("Select the option number: [Enter b to go back] [Enter q to exit]: ")
                
                if choice2.isdigit():
                    choice2 = int(choice2)

                    if 0 < choice2 <= len(second_list):
                        second_name = second_list[choice2 - 1]
                        func_num = zone[first_name][second_name][0]

                        if func_num == '1':
                            original_data=vc.record_voice()
                            vc.wav_generater(original_data,"original")
                            break

                        elif func_num == '2':
                            filename = input("please input the filename(Make sure the file is in the current path): ")
                            original_data=vc.read_wav_file(filename)
                            break
                        
                        elif func_num == '3':
                            if original_data is not None:
                                vc.play_audio(original_data)
                            else:
                                print("Please use Voice data processing input data first")
                                break

                        elif func_num == '4':
                            if original_data is not None:
                                data = vc.remove_noise(original_data)
                                gender,avg= vc.analyze_audio(data)

                                if gender=="Retry":
                                    print("Returning to the previous menu to re-enter data.")
                                    break
                                else: 
                                    g_data=vc.change_gender(data,gender=gender,avg_pitch=avg)
                                    vc.play_audio(g_data)
                                    vc.wav_generater(g_data,"Gender")
                            else:
                                print("Please use Voice data processing input data first")
                                break
 
                        elif func_num == '5':
                            if original_data is not None:
                                data = vc.remove_noise(original_data)
                                gender,avg= vc.analyze_audio(data)
                                if gender=="Retry":
                                    print("Returning to the previous menu to re-enter data.")
                                    break
                                else: 
                                    r_data=vc.robot_effect(data,gender=gender,avg_pitch=avg)
                                    vc.play_audio(r_data)
                                    vc.wav_generater(r_data,"Robot")
                            else:
                                print("Please use Voice data processing input data first")
                                break

                        elif func_num == '6':
                            if original_data is not None:
                                data = vc.remove_noise(original_data)
                                c_data=vc.child_effect(data)
                                vc.play_audio(c_data)
                                vc.wav_generater(c_data,"Child")
                            else:
                                print("Please use Voice data processing input data first")
                                break

                        else:
                            print("Exception !!!")
                    else:
                        print(f"\nInput {choice2} is not in the list! Please re-enter!\n")
                elif choice2 == "b":
                    break
                elif choice2 == "q":
                    exit()
                else:
                    print("\033[31mInput error, please re-enter!\033[0m")
        else:
            print(f"\nInput {choice1} is not in the list! Please re-enter!\n")
    elif choice1 == "q":
        exit()
    else:
        print("\033[31mInput error, please re-enter!\033[0m")