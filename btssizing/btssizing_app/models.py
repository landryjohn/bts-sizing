from django.db import models

# Create your models here.

class Projet(models.Model):
    titre = models.CharField("Titre", max_length=255)
    zone_geographique = models.CharField("Zone Géographique", max_length=255)
    description = models.CharField("Description du projet", max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    s_zone = models.FloatField(null=True)
    
class Plan_couverture(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True)
    pl_ul = models.FloatField(null=True)
    pout_ms = models.FloatField(null=True)
    pout_bs = models.FloatField(null=True)
    ga_bs = models.FloatField(null=True)
    ga_ms = models.FloatField(null=True)
    lf_bs = models.FloatField(null=True)
    lf_ms = models.FloatField(null=True)
    mf = models.FloatField(null=True)
    mi = models.FloatField(null=True)
    lp = models.FloatField(null=True)
    lb = models.FloatField(null=True)
    s_bs = models.FloatField(null=True)
    s_ms = models.FloatField(null=True)
    mpc = models.FloatField(null=True)
    eb_nt = models.FloatField(null=True)
    w = models.FloatField(null=True)
    rb = models.FloatField(null=True)
    kt = models.FloatField(null=True)
    pl_dl = models.FloatField(null=True)
    nf_bs = models.FloatField(null=True)
    pl = models.FloatField(null=True)
    modele_propagation = models.CharField(null=True, max_length=255)
    r = models.FloatField(null=True)
    hm = models.FloatField(null=True)
    hb = models.FloatField(null=True)
    heff = models.FloatField(null=True)
    ahm = models.FloatField(null=True)
    cm = models.FloatField(null=True)
    f = models.FloatField(null=True)
    s_cell_ul = models.FloatField(null=True)
    s_cell_dl = models.FloatField(null=True)
    d_inter_site = models.FloatField(null=True)
    n_site_ul = models.FloatField(null=True)
    n_site_dl = models.FloatField(null=True)
    nb_sites = models.IntegerField("Nombre de sites", null=True)
    created_at = models.DateTimeField(auto_now=True)

class Plan_capacite(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True)
    au = models.FloatField(null=True)
    u = models.FloatField(null=True)
    h = models.FloatField(null=True)
    pop_t_site = models.FloatField(null=True)
    nb_abonnes = models.FloatField(null=True)
    nb_sites = models.FloatField(null=True)

    nb_ab_msg = models.FloatField(null=True)
    p_msg = models.FloatField(null=True)

    nb_ab_nav = models.FloatField(null=True)
    p_nav = models.FloatField(null=True)

    nb_ab_rd = models.FloatField(null=True)
    p_rd = models.FloatField(null=True)

    nb_ab_voix = models.FloatField(null=True)
    p_voix = models.FloatField(null=True)

    d_ab_msg_ul = models.FloatField(null=True)
    d_msg_ul = models.FloatField(null=True)
    c_msg = models.FloatField(null=True)

    d_ab_nav_ul = models.FloatField(null=True)
    d_nav_ul = models.FloatField(null=True)
    c_nav = models.FloatField(null=True)

    d_ab_rd_ul = models.FloatField(null=True)
    d_rd_ul = models.FloatField(null=True)
    c_rd = models.FloatField(null=True)

    d_ab_voix_ul = models.FloatField(null=True)
    d_voix_ul = models.FloatField(null=True)
    c_voix = models.FloatField(null=True)

    d_ab_msg_dl = models.FloatField(null=True)
    d_msg_dl = models.FloatField(null=True)

    d_ab_nav_dl = models.FloatField(null=True)
    d_nav_dl = models.FloatField(null=True)

    d_ab_rd_dl = models.FloatField(null=True)
    d_rd_dl = models.FloatField(null=True)

    d_ab_voix_dl = models.FloatField(null=True)
    d_voix_dl = models.FloatField(null=True)

    d_total_msg_ul = models.FloatField(null=True)
    d_total_nav_ul = models.FloatField(null=True)
    d_total_rd_ul = models.FloatField(null=True)
    d_total_voix_ul = models.FloatField(null=True)

    d_total_msg_dl = models.FloatField(null=True)
    d_total_nav_dl = models.FloatField(null=True)
    d_total_rd_dl = models.FloatField(null=True)
    d_total_voix_dl = models.FloatField(null=True)

    d_total_ul = models.FloatField(null=True)
    d_total_dl = models.FloatField(null=True)

    nb_ab_ul = models.FloatField(null=True)
    debit_ul = models.FloatField(null=True)

    nb_ab_dl = models.FloatField(null=True)
    debit_dl = models.FloatField(null=True)

    nb_sites_ul = models.FloatField(null=True)
    nb_sites_dl = models.FloatField(null=True)

    nb_sites_capacite = models.FloatField(null=True)

    created_at = models.DateTimeField(auto_now=True)

