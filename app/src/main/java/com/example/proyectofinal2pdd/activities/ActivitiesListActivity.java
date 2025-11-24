package com.example.proyectofinal2pdd.activities;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.example.proyectofinal2pdd.MainActivity;
import com.example.proyectofinal2pdd.R;
import com.example.proyectofinal2pdd.api.RetrofitClient;
import com.example.proyectofinal2pdd.models.Activity;
import com.example.proyectofinal2pdd.utils.SessionManager;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ActivitiesListActivity extends AppCompatActivity {

    private RecyclerView recyclerView;
    private ActivitiesAdapter adapter;
    private List<Activity> activitiesList;
    private ProgressBar progressBar;
    private TextView tvEmptyState;
    private FloatingActionButton fabAdd;
    private SessionManager sessionManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_activities_list);

        // Inicializar SessionManager
        sessionManager = new SessionManager(this);

        // Configurar token en Retrofit
        String token = sessionManager.getAuthToken();
        if (token != null) {
            RetrofitClient.setAuthToken(token);
        }

        // Inicializar vistas
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);


        recyclerView = findViewById(R.id.recyclerView);
        progressBar = findViewById(R.id.progressBar);
        tvEmptyState = findViewById(R.id.tvEmptyState);
        fabAdd = findViewById(R.id.fabAdd);

        // Configurar RecyclerView
        activitiesList = new ArrayList<>();
        adapter = new ActivitiesAdapter(activitiesList, this);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(adapter);

        // Listeners del adapter
        adapter.setOnItemClickListener(new ActivitiesAdapter.OnItemClickListener() {
            @Override
            public void onEditClick(Activity activity) {
                showEditDialog(activity);
            }

            @Override
            public void onDeleteClick(Activity activity) {
                confirmDelete(activity);
            }
        });

        // Click en FAB para agregar
        fabAdd.setOnClickListener(v -> showAddDialog());

        // Cargar actividades
        loadActivities();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == R.id.action_logout) {
            logout();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void loadActivities() {
        progressBar.setVisibility(View.VISIBLE);
        tvEmptyState.setVisibility(View.GONE);

        Call<List<Activity>> call = RetrofitClient.getApiService().getActivities();
        call.enqueue(new Callback<List<Activity>>() {
            @Override
            public void onResponse(Call<List<Activity>> call, Response<List<Activity>> response) {
                progressBar.setVisibility(View.GONE);

                if (response.isSuccessful() && response.body() != null) {
                    activitiesList.clear();
                    activitiesList.addAll(response.body());
                    adapter.notifyDataSetChanged();

                    if (activitiesList.isEmpty()) {
                        tvEmptyState.setVisibility(View.VISIBLE);
                    }
                } else {
                    Toast.makeText(ActivitiesListActivity.this, "Error al cargar actividades", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Activity>> call, Throwable t) {
                progressBar.setVisibility(View.GONE);
                Toast.makeText(ActivitiesListActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void showAddDialog() {
        CreateActivityDialog dialog = new CreateActivityDialog(this, null, new CreateActivityDialog.OnActivitySavedListener() {
            @Override
            public void onActivitySaved() {
                loadActivities(); // Recargar lista
            }
        });
        dialog.show();
    }

    private void showEditDialog(Activity activity) {
        CreateActivityDialog dialog = new CreateActivityDialog(this, activity, new CreateActivityDialog.OnActivitySavedListener() {
            @Override
            public void onActivitySaved() {
                loadActivities(); // Recargar lista
            }
        });
        dialog.show();
    }

    private void confirmDelete(Activity activity) {
        new AlertDialog.Builder(this)
                .setTitle("Eliminar actividad")
                .setMessage("¿Estás seguro de eliminar esta actividad?")
                .setPositiveButton("Eliminar", (dialog, which) -> deleteActivity(activity))
                .setNegativeButton("Cancelar", null)
                .show();
    }

    private void deleteActivity(Activity activity) {
        progressBar.setVisibility(View.VISIBLE);

        Call<Void> call = RetrofitClient.getApiService().deleteActivity(activity.getId());
        call.enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                progressBar.setVisibility(View.GONE);

                if (response.isSuccessful()) {
                    Toast.makeText(ActivitiesListActivity.this, "Actividad eliminada", Toast.LENGTH_SHORT).show();
                    loadActivities();
                } else {
                    Toast.makeText(ActivitiesListActivity.this, "Error al eliminar", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Void> call, Throwable t) {
                progressBar.setVisibility(View.GONE);
                Toast.makeText(ActivitiesListActivity.this, "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void logout() {
        sessionManager.logout();
        Intent intent = new Intent(this, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(intent);
        finish();
    }

    @Override
    protected void onResume() {
        super.onResume();
        loadActivities();
    }
}