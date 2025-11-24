package com.example.proyectofinal2pdd.activities;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;

import com.example.proyectofinal2pdd.R;
import com.example.proyectofinal2pdd.api.RetrofitClient;
import com.example.proyectofinal2pdd.models.Activity;
import com.google.android.material.textfield.TextInputEditText;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CreateActivityDialog extends Dialog {

    private TextInputEditText etType, etDuration, etDate, etNotes;
    private RadioGroup rgIntensity;
    private RadioButton rbBaja, rbMedia, rbAlta;
    private Button btnSave, btnCancel;
    private TextView tvTitle;

    private Activity activityToEdit;
    private OnActivitySavedListener listener;

    public interface OnActivitySavedListener {
        void onActivitySaved();
    }

    public CreateActivityDialog(@NonNull Context context, Activity activity, OnActivitySavedListener listener) {
        super(context);
        this.activityToEdit = activity;
        this.listener = listener;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.dialog_create_activity);

        // Inicializar vistas
        tvTitle = findViewById(R.id.tvTitle);
        etType = findViewById(R.id.etType);
        etDuration = findViewById(R.id.etDuration);
        etDate = findViewById(R.id.etDate);
        etNotes = findViewById(R.id.etNotes);
        rgIntensity = findViewById(R.id.rgIntensity);
        rbBaja = findViewById(R.id.rbBaja);
        rbMedia = findViewById(R.id.rbMedia);
        rbAlta = findViewById(R.id.rbAlta);
        btnSave = findViewById(R.id.btnSave);
        btnCancel = findViewById(R.id.btnCancel);

        // Si es edición, llenar campos
        if (activityToEdit != null) {
            tvTitle.setText("Editar Actividad");
            etType.setText(activityToEdit.getType());
            etDuration.setText(String.valueOf(activityToEdit.getDurationMinutes()));
            etDate.setText(activityToEdit.getDate().substring(0, 10));
            etNotes.setText(activityToEdit.getNotes());

            switch (activityToEdit.getIntensity().toLowerCase()) {
                case "baja":
                    rbBaja.setChecked(true);
                    break;
                case "media":
                    rbMedia.setChecked(true);
                    break;
                case "alta":
                    rbAlta.setChecked(true);
                    break;
            }
        } else {
            // Fecha de hoy por defecto
            String today = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(new Date());
            etDate.setText(today);
        }

        // Listeners
        btnSave.setOnClickListener(v -> saveActivity());
        btnCancel.setOnClickListener(v -> dismiss());
        // Hacer el diálogo más ancho
        if (getWindow() != null) {
            getWindow().setLayout(
                    (int) (getContext().getResources().getDisplayMetrics().widthPixels * 0.95), // 95% del ancho de la pantalla
                    ViewGroup.LayoutParams.WRAP_CONTENT
            );
        }
    }

    private void saveActivity() {
        String type = etType.getText().toString().trim();
        String durationStr = etDuration.getText().toString().trim();
        String date = etDate.getText().toString().trim();
        String notes = etNotes.getText().toString().trim();

        // Validaciones
        if (type.isEmpty()) {
            etType.setError("Ingresa el tipo");
            return;
        }

        if (durationStr.isEmpty()) {
            etDuration.setError("Ingresa la duración");
            return;
        }

        if (date.isEmpty()) {
            etDate.setError("Ingresa la fecha");
            return;
        }

        int duration = Integer.parseInt(durationStr);

        // Obtener intensidad seleccionada
        int selectedId = rgIntensity.getCheckedRadioButtonId();
        String intensity = "Media";
        if (selectedId == R.id.rbBaja) {
            intensity = "Baja";
        } else if (selectedId == R.id.rbMedia) {
            intensity = "Media";
        } else if (selectedId == R.id.rbAlta) {
            intensity = "Alta";
        }

        // Crear objeto Activity
        Activity activity = new Activity(type, duration, date, intensity, notes);

        // Llamada a la API
        if (activityToEdit != null) {
            // Editar
            updateActivity(activityToEdit.getId(), activity);
        } else {
            // Crear
            createActivity(activity);
        }
    }

    private void createActivity(Activity activity) {
        Call<Activity> call = RetrofitClient.getApiService().createActivity(activity);
        call.enqueue(new Callback<Activity>() {
            @Override
            public void onResponse(Call<Activity> call, Response<Activity> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(getContext(), "Actividad creada", Toast.LENGTH_SHORT).show();
                    if (listener != null) {
                        listener.onActivitySaved();
                    }
                    dismiss();
                } else {
                    Toast.makeText(getContext(), "Error al crear", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Activity> call, Throwable t) {
                Toast.makeText(getContext(), "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void updateActivity(int id, Activity activity) {
        Call<Activity> call = RetrofitClient.getApiService().updateActivity(id, activity);
        call.enqueue(new Callback<Activity>() {
            @Override
            public void onResponse(Call<Activity> call, Response<Activity> response) {
                if (response.isSuccessful()) {
                    Toast.makeText(getContext(), "Actividad actualizada", Toast.LENGTH_SHORT).show();
                    if (listener != null) {
                        listener.onActivitySaved();
                    }
                    dismiss();
                } else {
                    Toast.makeText(getContext(), "Error al actualizar", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<Activity> call, Throwable t) {
                Toast.makeText(getContext(), "Error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }
}