import voice_changer as vc

def main():
    print("Original male_test voice:")
    male_data = vc.read_wav_file('male_test.wav')
    vc.play_audio(male_data)
    
    print("Original female_test voice:")
    female_data = vc.read_wav_file('female_test.wav')
    vc.play_audio(female_data)
    
    male_data = vc.remove_noise(male_data)
    female_data = vc.remove_noise(female_data)

    print("Analyzing male voice:")
    gender1, avg1 = vc.analyze_audio(male_data)
    print(f"Recognized as: {gender1}, averge pitch is: {int(avg1)}")
    
    print("Analyzing female voice:")
    gender2, avg2 = vc.analyze_audio(female_data)
    print(f"Recognized as: {gender2}, averge pitch is: {int(avg2)}")

    print("Changing male voice to female:")
    changed_data1 = vc.change_gender(male_data, gender1, avg1)  
    vc.play_audio(changed_data1)

    print("Changing female voice to male:")
    changed_data2 = vc.change_gender(female_data, gender2, avg2)  
    vc.play_audio(changed_data2)
    
    print("Applying robot effect to female voice:")
    robot_data = vc.robot_effect(female_data,gender=gender2,avg_pitch=avg2)
    vc.play_audio(robot_data)
    
    print("Applying child effect to female voice:")
    child_data = vc.child_effect(female_data)
    vc.play_audio(child_data)
    
if __name__ == "__main__":
    main()