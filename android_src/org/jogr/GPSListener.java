package org.jogr;

import android.location.Location;
import android.location.LocationListener;
import android.os.Bundle;

public class GPSListener implements LocationListener {

    private final Runnable callback;

    private double latitude = 0.0;
    private double longitude = 0.0;
    private float speed = 0.0f;
    private float bearing = 0.0f;
    private double altitude = 0.0;
    private float accuracy = 0.0f;

    public GPSListener(Runnable callback) {
        this.callback = callback;
    }

    private void processLocation(Location location) {
        if (location == null) {
            return;
        }

        latitude = location.getLatitude();
        longitude = location.getLongitude();
        speed = location.getSpeed();
        bearing = location.getBearing();
        altitude = location.getAltitude();
        accuracy = location.getAccuracy();

        android.util.Log.d(
            "JogR_GPS",
            "LOCATION: lat=" + latitude
            + ", lon=" + longitude
        );

        if (callback != null) {
            callback.run();
        }
    }

    @Override
    public void onLocationChanged(Location location) {
        processLocation(location);
    }

    @Override
    public void onLocationChanged(java.util.List<Location> locations) {
        if (locations == null || locations.isEmpty()) {
            return;
        }

        for (Location location : locations) {
            processLocation(location);
        }
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public float getSpeed() {
        return speed;
    }

    public float getBearing() {
        return bearing;
    }

    public double getAltitude() {
        return altitude;
    }

    public float getAccuracy() {
        return accuracy;
    }

    @Override
    public void onProviderEnabled(String provider) {
    }

    @Override
    public void onProviderDisabled(String provider) {
    }

    @Override
    public void onStatusChanged(
        String provider,
        int status,
        Bundle extras
    ) {
    }
}
