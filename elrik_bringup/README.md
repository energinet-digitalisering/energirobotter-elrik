# Elrik Bringup

Bringup package for Elrik, with different launch scripts for each mode/feature.

## Teleoperation

### Setup VR Headset

1. Turn on headset
2. Plug USB cable into headset first, then put it on
3. Plug cable into computer, and accept USB connection in the headset
> If the "`USB-C Port Disabled, water and debris`" message pops up, restart the headset and try again. If that does not work, use the other end of the cable and try again.
4. From terminal on PC, enable reverse port forwarding:
   ```
   adb reverse tcp:8012 tcp:8012
   ```


### Setup Teleoperation

1. In a teminal on the computer, open RViz2 with config file:
   ```
   rviz2 -d src/energirobotter-elrik/elrik_bringup/config/rviz/teleoperation.rviz
   ```
2. In another terminal, run teleoperation (and IK but no camera) with:
   ```
   ros2 launch elrik_bringup teleoperation.launch.py camera_enabled:=false rviz:=false
   ```
3. In the headset's browser, go to the adress: `127.0.0.1:8012`

### Setup Elrik

1. Turn on Elrik
2. On your phone, connect to the `ESP32_DEV` Wi-Fi network
3. In browser, go to `192.168.4.1`
4. Click button `Start Serial Forwarding` - OBS! Make sure nothing is sending commands to Elrik yet
5. Click botton `Stop Serial Forwarding` but don't click `OK`, it's now ready as a stop button if needed
6. From terminal on PC SSH into Elrik:
   ```
   ssh elrik@192.168.1.101
   ```

### Calibrate and Launch

1. In the headset, press "passthrough"
2. Calibrate the view (hold down Meta button on right controller)
3. Verify that tracking is working in RViz
4. Start `arm.launch.py`:
   >Make sure the VR is tracking properly! As soon as the `arm.launch.py` is running, it will start moving!
   ```
   cd energinet/
   shumble
   sw
   ros2 launch elrik_bringup arm.launch.py
   ```
   
5. When done with the teleoperation, stop the `arm.launch.py` terminal

---

### V1 Demo notes (Danish):

Der er nogle ting vi skal gøre brugere opmærksomme på: 
- Pas på ledningen!
- Bevæg ikke hovedet for meget, trackingen vil drifte!
- Start langsomt, få en fornemmelse for hvordan Elrik reagerer
- Der er ikke noget der stopper armene fra at kollidere med hinanden, så vær forsigtig 
- Sig til når man er done, programmet skal stoppes før headset kommer af

Steps: 
- Sæt streaming op på computer, så andre kan se med 
- Start med at tage headset på, og sikre at det sidder godt 
- Kalibrér med højre controller 
- Tjek at de kan se igennem 
- Tjek tracking i RViz 
- Hænderne på bordet (eller bare stille foran én) 
- Start programmet! 
- Vær klar til at stoppe, hvis der sker noget, eller de tager headset af for hurtigt
