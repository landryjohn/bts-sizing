import json
import math
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import Plan_capacite, Plan_couverture, Projet

# Vue index
def index(request): 
    return redirect('home/')

@login_required
def dashboard(request):
    return render(request, 'btssizing_app/index.html')

@login_required
def projects(request):
    projects = Projet.objects.all()
    print(json.dumps(list(Projet.objects.values('id', 'titre', 'zone_geographique', 's_zone', 'description'))))
    return render(request, 
        'btssizing_app/projects.html', 
        context={
            'projects':list(projects),
            'json_projects':json.dumps(list(Projet.objects.values('id', 'titre', 'zone_geographique', 's_zone', 'description')))
            }
        )

@login_required
def plan_couverture(request):
    plans = Plan_couverture.objects.filter(projet__isnull=False)
    return render(request, 'btssizing_app/plan_couverture.html', {'plans':plans})

@login_required
def add_plan_couverture(request):
    # recuperatopm de la liste de tous les projets
    projects = list(Projet.objects.all())
    step = request.POST.get('step', None) 
    # print("request.POST =>", end='')
    # print(request.POST)
    if step == '1' :
        # recuperation de toutes la valeurs poste par l'utilisateur 
        data = request.POST
        if not data.get('id', None) :
            return HttpResponseBadRequest("Oups, Bad request...")
        data = {k:float(v) for k,v in data.items() if isfloat(v)}
        p_c = Plan_couverture.objects.get(id=int(data['id']))
        p_c.projet = Projet.objects.get(id=int(data['project_id']))
        p_c.pout_ms = data['pout_ms']
        p_c.pout_bs = data['pout_bs']
        p_c.ga_bs = data['ga_bs']
        p_c.ga_ms = data['ga_ms']
        p_c.lf_bs = data['lf_bs']
        p_c.lf_ms = data['lf_ms']
        p_c.mf = data['mf']
        p_c.mi = data['mi']
        p_c.lp = data['lp']
        p_c.lb = data['lb']
        p_c.s_bs = data['s_bs']
        p_c.s_ms = data['s_ms']
        p_c.mpc = data['mpc']
        # 1 : Calcul du bilan de liaison sur le lien montant
        p_c.pl_ul = p_c.pout_ms + p_c.ga_bs + p_c.ga_ms - p_c.lf_bs - p_c.mf - p_c.mi - p_c.lp - p_c.lb - p_c.s_bs - p_c.mpc
        
        # 2 : Calcul du bilan de liaison sur le lien descendant
        p_c.pl_dl = p_c.pout_bs + p_c.ga_bs + p_c.ga_ms - p_c.lf_ms - p_c.mf - p_c.mi - p_c.lp - p_c.lb - p_c.s_ms - p_c.mpc
        
        # 3 : Calcul du bilan de liaison
        p_c.pl = min(p_c.pl_ul, p_c.pl_ul) 

        # Sauvegarde en base de donnees 
        p_c.save()
        return render(
            request, 
            'btssizing_app/add_plan_couverture.html', 
            context={'step':2, 'step_name':'Finalisation de la planification',
                'projects':projects, 'id':p_c.id, 'p_c':p_c
            }
        )
    elif step == '2' :
        data = request.POST
        data = {k:(float(v) if isfloat(v) else v) for k,v in data.items()}
        p_c = Plan_couverture.objects.get(id=int(data['id']))
        p_c.modele_propagation = data['modele_propagation']
        p_c.f = data['f']
        p_c.hb = data['hb']
        p_c.hm = data['hm']
        p_c.heff = data['heff']
        p_c.ahm = data['ahm']
        p_c.cm = data['cm']
        
        # 4 : Choix du modèle de propagation
        p_c.modele_propagation = data['modele_propagation']
        print("Modele de propagation =>", p_c.modele_propagation)
        # 5 : Calcul du rayon
        if p_c.modele_propagation == "PEL" :
            # Propagation en espace libre
            p_c.r = pow(10, ( p_c.pl - 32.4 - 20*math.log(p_c.f,10) )/20 ) 
        elif p_c.modele_propagation == "MOH" :
            # Modèle Okumura-Hata
            p_c.r = pow(10, (p_c.pl - 69.55 - 26.16*math.log(p_c.f) + p_c.ahm + 4.78*((math.log(p_c.f, 10))**2) - 18.33*math.log(p_c.f,10) + 35.94)/(44.9 - 6.55*math.log(p_c.hb, 10)) )
        elif p_c.modele_propagation == "MCH" :
            # Modèle Cost231-Hata
            p_c.r = pow(10, (p_c.pl - 46.3 - 33.9*math.log(p_c.f,10) + 13.82*math.log(p_c.hb, 10) + p_c.ahm - p_c.cm )/(44.9 - 6.55*math.log(p_c.hb, 10)) )
        elif p_c.modele_propagation == "MSGKF" :
            # Modèles Software Général (K-facteur)
            k1,k2,k3,k4,k5,k6,k7,kclutter = 145, 44.9, -2.49, 0.00, -13.82, -6.55, -0.8, -2.90
            p_c.r = pow(10, (p_c.pl - k1 - k3*p_c.hm - k4*math.log(p_c.hm) - k5*math.log(p_c.heff) - k7 - kclutter)/(k2+ k6*math.log(p_c.heff, 10)))

        # 6 : Determinsation de la surface de la cellule 
        p_c.s_cell_ul = 2.6*(p_c.r**2)
        p_c.s_cell_dl = 1.95*2.6*(p_c.r**2)

        # 7 : Nombre de BTS
        projet = Projet.objects.get(id=p_c.projet.id)
        p_c.n_site_ul = projet.s_zone / p_c.s_cell_ul
        p_c.n_site_dl = projet.s_zone / p_c.s_cell_dl
        p_c.nb_sites = max(p_c.n_site_ul, p_c.n_site_dl)
        p_c.save()
        return render(
            request, 
            'btssizing_app/result_plan_couverture.html',
            context={'p_c':p_c}
        )
    else :
        plan_couverture = Plan_couverture.objects.create()
        # p_c = Plan_couverture.objects.get(id=1)
        return render(
            request, 
            'btssizing_app/add_plan_couverture.html', 
            context={'step':1, 'step_name':'Calcul du bilan de liaison',
                'projects':projects, 
                # 'id':1,
                'id':plan_couverture.id,
                'p_c': plan_couverture
            }
        )

@login_required
def show_plan_couverture(request, id):
    try : 
        p_c = Plan_couverture.objects.get(id=id)
    except :
        return HttpResponseBadRequest("Bad request : Le plan de couverture n'existe pas")
    return render(
        request, 
        'btssizing_app/result_plan_couverture.html',
        context={'p_c':p_c}
    )

@login_required
def add_project(request):
    payload = request.POST
    # create the project
    project = Projet.objects.create(
        titre=payload['title'],
        zone_geographique=payload['zone'], 
        s_zone=payload['surface_zone'],
        description=payload['description']
    )
    project.save()
    return redirect("btssizing_app:projects")

@login_required
def edit_plan_couverture(request, id):
    try : 
        p_c = Plan_couverture.objects.get(id=id)
        projects = list(Projet.objects.all())
    except :
        return HttpResponseBadRequest("Le plan de couverture choisi n'existe pas.")
    return render(
        request, 
        'btssizing_app/add_plan_couverture.html', 
        context={'step':1, 'step_name':'Calcul du bilan de liaison',
            'projects':projects, 
            'id':id,
            'p_c': p_c
        }
    )

@login_required
def plan_capacite(request):
    plans = Plan_capacite.objects.filter(projet__isnull=False)
    return render(request, 'btssizing_app/plan_capacite.html', {'plans':plans})

@login_required
def edit_plan_capacite(request, id):
    try : 
        p_ca = Plan_capacite.objects.get(id=id)
        projects = list(Projet.objects.all())
    except :
        return HttpResponseBadRequest("Le plan de capacité choisi n'existe pas.")
    return render(
        request, 
        'btssizing_app/add_plan_capacite.html', 
        context={
            'projects':projects, 
            'id':id,
            'p_ca': p_ca
        }
    )

@login_required
def add_plan_capacite(request):
    # recuperatopm de la liste de tous les projets
    projects = list(Projet.objects.all())
    # recuperation de toutes la valeurs poste par l'utilisateur 
    id = request.POST.get('id', None) 
    if id != None :
        data = request.POST
        if not data.get('id', None) :
            return HttpResponseBadRequest("Oups, Bad request...")
        data = {k:float(v) for k,v in data.items() if isfloat(v)}
        p_ca = Plan_capacite.objects.get(id=int(data['id']))
        p_ca.projet = Projet.objects.get(id=int(data['project_id']))
        
        # 1. Calcul de L’intensité de trafic par utilisateur 
        p_ca.u = data['u']
        p_ca.h = data['h']
        p_ca.au = p_ca.u * p_ca.h 

        # 2. Calcul de la population totale /site (2)
        p_ca.nb_abonnes = data['nb_abonnes']
        p_ca.nb_sites = data['nb_sites']
        p_ca.pop_t_site = p_ca.nb_abonnes / p_ca.nb_sites

        # 3. Nombre d’abonnés par service (3)
        p_ca.p_msg = data['p_msg']
        p_ca.p_nav = data['p_nav']
        p_ca.p_rd = data['p_rd']
        p_ca.p_voix = data['p_voix']

        p_ca.nb_ab_msg = (p_ca.p_msg * p_ca.nb_abonnes) / 100
        p_ca.nb_ab_nav = (p_ca.p_nav * p_ca.nb_abonnes) / 100
        p_ca.nb_ab_rd = (p_ca.p_rd * p_ca.nb_abonnes) / 100
        p_ca.nb_ab_voix = (p_ca.p_voix * p_ca.nb_abonnes) / 100

        # 4.	Débit par abonné pour chaque service 
        p_ca.d_msg_ul = data['d_msg_ul']
        p_ca.c_msg = data['c_msg']
        p_ca.d_nav_ul = data['d_nav_ul']
        p_ca.c_nav = data['c_nav']
        p_ca.d_rd_ul = data['d_rd_ul']
        p_ca.c_rd = data['c_rd']
        p_ca.d_voix_ul = data['d_voix_ul']
        p_ca.c_voix = data['c_voix']

        p_ca.d_ab_msg_ul = (p_ca.d_msg_ul * p_ca.c_msg) / 100
        p_ca.d_ab_nav_ul = (p_ca.d_nav_ul * p_ca.c_nav) / 100
        p_ca.d_ab_rd_ul = (p_ca.d_rd_ul * p_ca.c_rd) / 100
        p_ca.d_ab_voix_ul = (p_ca.d_voix_ul * p_ca.c_voix) / 100
        
        # Dowlink
        p_ca.d_msg_dl = data['d_msg_dl']
        p_ca.d_nav_dl = data['d_nav_dl']
        p_ca.d_rd_dl = data['d_rd_dl']
        p_ca.d_voix_dl = data['d_voix_dl']

        p_ca.d_ab_msg_dl = (p_ca.d_msg_dl * p_ca.c_msg) / 100
        p_ca.d_ab_nav_dl = (p_ca.d_nav_dl * p_ca.c_nav) / 100
        p_ca.d_ab_rd_dl = (p_ca.d_rd_dl * p_ca.c_rd) / 100
        p_ca.d_ab_voix_dl = (p_ca.d_voix_dl * p_ca.c_voix) / 100
        
        # 5. Débit total de chaque service (4)
        p_ca.d_total_msg_ul = p_ca.d_ab_msg_ul * p_ca.nb_ab_msg 
        p_ca.d_total_nav_ul = p_ca.d_ab_nav_ul * p_ca.nb_ab_nav 
        p_ca.d_total_rd_ul = p_ca.d_ab_rd_ul * p_ca.nb_ab_rd 
        p_ca.d_total_voix_ul = p_ca.d_ab_voix_ul * p_ca.nb_ab_voix

        p_ca.d_total_msg_dl = p_ca.d_ab_msg_dl * p_ca.nb_ab_msg 
        p_ca.d_total_nav_dl = p_ca.d_ab_nav_dl * p_ca.nb_ab_nav 
        p_ca.d_total_rd_dl = p_ca.d_ab_rd_dl * p_ca.nb_ab_rd 
        p_ca.d_total_voix_dl = p_ca.d_ab_voix_dl * p_ca.nb_ab_voix

        # 6. Débit global utilisateur /classe de service (DL/UL) (5)
        p_ca.d_total_ul = p_ca.d_total_msg_ul + p_ca.d_total_nav_ul + p_ca.d_total_rd_ul + p_ca.d_total_voix_ul 
        p_ca.d_total_dl = p_ca.d_total_msg_dl + p_ca.d_total_nav_dl + p_ca.d_total_rd_dl + p_ca.d_total_voix_dl 
        
        # 7. Nombre d’abonnés/site
        p_ca.debit_ul = data['debit_ul']
        p_ca.nb_ab_ul = p_ca.d_total_ul / (p_ca.debit_ul * 1000)
        
        p_ca.debit_dl = data['debit_dl']
        p_ca.nb_ab_dl = p_ca.d_total_dl / (p_ca.debit_dl * 1000)
        
        # 8. Nombre de site (6)
        p_ca.nb_sites_ul = p_ca.nb_abonnes /  p_ca.nb_ab_ul
        p_ca.nb_sites_dl = p_ca.nb_abonnes /  p_ca.nb_ab_dl
        
        p_ca.nb_sites_capacite = min(p_ca.nb_sites_ul, p_ca.nb_sites_dl)

        p_ca.save()
        return render(
            request, 
            'btssizing_app/result_plan_capacite.html',
            context={'p_ca':p_ca}
        )
    else :
        # plan_capacite = Plan_capacite.objects.create()
        plan_capacite = Plan_capacite.objects.get(id=1)
        return render(
            request, 
            'btssizing_app/add_plan_capacite.html', 
            context={
                'projects':projects, 
                # 'id':1,
                'id':plan_capacite.id,
                'p_ca': plan_capacite
            }
        )

@login_required
def show_plan_capacite(request, id):
    try : 
        p_ca = Plan_capacite.objects.get(id=id)
    except :
        return HttpResponseBadRequest("Bad request : Le plan de capacité n'existe pas")
    return render(
        request, 
        'btssizing_app/result_plan_capacite.html',
        context={'p_ca':p_ca}
    )

@login_required
def users(request):
    return redirect("btssizing_app:home") ; 
    # users = UserModel.objects.all()
    # return render(request, 'btssizing_app/users.html', {'users':users})


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False