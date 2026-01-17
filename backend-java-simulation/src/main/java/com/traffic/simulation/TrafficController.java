package com.traffic.simulation;

import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;

@RestController
@RequestMapping("/api/traffic")
@CrossOrigin(origins = "*") // Allows Python to access this API
public class TrafficController {

    // --- SIMULATION STATE ---
    private int northCars = 10;
    private int eastCars = 10;
    private String currentGreenLight = "NORTH"; 

    // 1. GET API: Python calls this to "Look" at traffic
    @GetMapping("/state")
    public Map<String, Object> getState() {
        // Simulate random cars arriving
        addRandomTraffic();
        
        Map<String, Object> state = new HashMap<>();
        state.put("north_cars", northCars);
        state.put("east_cars", eastCars);
        state.put("current_green", currentGreenLight);
        return state;
    }

    // 2. POST API: Python calls this to "Switch" lights
    @PostMapping("/action")
    public String performAction(@RequestBody Map<String, Integer> actionMap) {
        int action = actionMap.getOrDefault("action", 0);

        if (action == 1) {
            switchLight();
        }
        
        // Simulate cars leaving if light is green
        processTrafficFlow();
        
        // Print status to terminal so you can see it working
        System.out.println("Java Backend -> North: " + northCars + " | East: " + eastCars + " | Green: " + currentGreenLight);
        return "Executed";
    }

    // --- HELPER LOGIC ---
    private void switchLight() {
        if (currentGreenLight.equals("NORTH")) {
            currentGreenLight = "EAST";
        } else {
            currentGreenLight = "NORTH";
        }
    }

    private void processTrafficFlow() {
        if (currentGreenLight.equals("NORTH")) {
            northCars = Math.max(0, northCars - 5); 
        } else {
            eastCars = Math.max(0, eastCars - 5);
        }
    }

    private void addRandomTraffic() {
        Random rand = new Random();
        northCars += rand.nextInt(3); 
        eastCars += rand.nextInt(3);
    }
}