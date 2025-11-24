package com.example.proyectofinal2pdd.activities;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.example.proyectofinal2pdd.R;
import com.example.proyectofinal2pdd.models.Activity;

import java.util.List;

public class ActivitiesAdapter extends RecyclerView.Adapter<ActivitiesAdapter.ViewHolder> {

    private List<Activity> activities;
    private Context context;
    private OnItemClickListener listener;

    public interface OnItemClickListener {
        void onEditClick(Activity activity);
        void onDeleteClick(Activity activity);
    }

    public void setOnItemClickListener(OnItemClickListener listener) {
        this.listener = listener;
    }

    public ActivitiesAdapter(List<Activity> activities, Context context) {
        this.activities = activities;
        this.context = context;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_activity, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        Activity activity = activities.get(position);

        holder.tvType.setText(activity.getType());
        holder.tvDuration.setText(activity.getDurationMinutes() + " minutos");
        holder.tvDate.setText(activity.getDate().substring(0, 10)); // Solo la fecha
        holder.tvIntensity.setText(activity.getIntensity());

        // Mostrar notas si existen
        if (activity.getNotes() != null && !activity.getNotes().isEmpty()) {
            holder.tvNotes.setVisibility(View.VISIBLE);
            holder.tvNotes.setText(activity.getNotes());
        } else {
            holder.tvNotes.setVisibility(View.GONE);
        }

        // Color según intensidad
        switch (activity.getIntensity().toLowerCase()) {
            case "alta":
                holder.tvIntensity.setTextColor(context.getResources().getColor(android.R.color.holo_red_dark));
                break;
            case "media":
                holder.tvIntensity.setTextColor(context.getResources().getColor(android.R.color.holo_orange_dark));
                break;
            case "baja":
                holder.tvIntensity.setTextColor(context.getResources().getColor(android.R.color.holo_green_dark));
                break;
        }

        // Clicks
        holder.btnEdit.setOnClickListener(v -> {
            if (listener != null) {
                listener.onEditClick(activity);
            }
        });

        holder.btnDelete.setOnClickListener(v -> {
            if (listener != null) {
                listener.onDeleteClick(activity);
            }
        });
    }

    @Override
    public int getItemCount() {
        return activities.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView tvType, tvDuration, tvDate, tvIntensity, tvNotes;
        ImageButton btnEdit, btnDelete;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            tvType = itemView.findViewById(R.id.tvType);
            tvDuration = itemView.findViewById(R.id.tvDuration);
            tvDate = itemView.findViewById(R.id.tvDate);
            tvIntensity = itemView.findViewById(R.id.tvIntensity);
            tvNotes = itemView.findViewById(R.id.tvNotes);
            btnEdit = itemView.findViewById(R.id.btnEdit);
            btnDelete = itemView.findViewById(R.id.btnDelete);
        }
    }
}