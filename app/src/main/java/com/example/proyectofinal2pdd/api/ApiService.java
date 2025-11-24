package com.example.proyectofinal2pdd.api;

import com.example.proyectofinal2pdd.models.Activity;
import com.example.proyectofinal2pdd.models.AuthResponse;
import com.example.proyectofinal2pdd.models.User;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.PATCH;
import retrofit2.http.POST;
import retrofit2.http.Path;

public interface ApiService {

    // Autenticación
    @POST("auth/sign-in")
    Call<AuthResponse> signIn(@Body User user);

    @POST("auth/sign-up")
    Call<AuthResponse> signUp(@Body User user);

    // Actividades
    @GET("activities")
    Call<List<Activity>> getActivities();

    @GET("activities/{id}")
    Call<Activity> getActivityById(@Path("id") int id);

    @POST("activities")
    Call<Activity> createActivity(@Body Activity activity);

    @PATCH("activities/{id}")
    Call<Activity> updateActivity(@Path("id") int id, @Body Activity activity);

    @DELETE("activities/{id}")
    Call<Void> deleteActivity(@Path("id") int id);
}