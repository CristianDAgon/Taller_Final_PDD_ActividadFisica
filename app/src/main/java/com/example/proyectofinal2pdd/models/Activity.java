package com.example.proyectofinal2pdd.models;

public class Activity {
    private int id;
    private String type;
    private int durationMinutes;
    private String date;
    private String intensity;
    private String notes;  // NUEVO: campo notes

    // Constructor vacío
    public Activity() {
    }

    // Constructor completo
    public Activity(String type, int durationMinutes, String date, String intensity, String notes) {
        this.type = type;
        this.durationMinutes = durationMinutes;
        this.date = date;
        this.intensity = intensity;
        this.notes = notes;
    }

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getDurationMinutes() {
        return durationMinutes;
    }

    public void setDurationMinutes(int durationMinutes) {
        this.durationMinutes = durationMinutes;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getIntensity() {
        return intensity;
    }

    public void setIntensity(String intensity) {
        this.intensity = intensity;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }
}