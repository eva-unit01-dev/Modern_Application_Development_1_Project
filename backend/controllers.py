
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import current_app as app #ALIAS FOR CURRENT RUNNING APP
from .models import *
from datetime import datetime, timezone

#@app.route("/")
#def home():
#    return "<h2>WELCOME TO SYNCIT</h2>"


##LANDING PAGE/HOME PAGE##
@app.route("/", methods=['GET','POST']) #REFERS URL 127.0.0.1:5000
def home():
    return render_template("index.html")

##################################S P O N S O R##################################



##REGISTRATION FOR SPONSORS##
@app.route("/sponsor_registration", methods=['GET','POST'])
def sponsor_registration():
    if request.method=="POST":
        spon_type=request.form.get("type")
        email=request.form.get("email")
        spon_full_name=request.form.get("name")
        spon_user_name=request.form.get("uname")
        industry=request.form.get("industry")
        evaluation=request.form.get("evaluation")
        spon_password=request.form.get("password")
        usr1=spon_info.query.filter_by(spon_user_name=spon_user_name).first()
        if not usr1:
            new_usr1=spon_info(spon_type=spon_type, email=email, spon_full_name=spon_full_name, spon_user_name=spon_user_name, industry=industry, evaluation=evaluation, spon_password=spon_password)
            db.session.add(new_usr1)
            db.session.commit()
            return render_template("sponsor_login.html")
        else:
            return render_template("index.html")
    return render_template("sponsor_registration.html")



##LOGIN FOR SPONSORS##
@app.route("/sponsor_login", methods=['GET','POST'])
def sponsor_login():
    if request.method == "POST":
        spon_user_name = request.form.get("uname")
        spon_password = request.form.get("password")
        this_usr1 = spon_info.query.filter_by(spon_user_name=spon_user_name).first()
        
        if this_usr1 and this_usr1.spon_password == spon_password:
            session['spon_user_name'] = spon_user_name
            return redirect(url_for("sponsor_dashboard"))
        else:
            flash("Invalid username or password", "error")
    
    return render_template("sponsor_login.html")



'''
@app.route("/sponsor_login", methods=['GET','POST'])
def sponsor_login():
    if request.method=="POST":
        spon_user_name=request.form.get("uname")
        spon_password=request.form.get("password")
        this_usr1=spon_info.query.filter_by(spon_user_name=spon_user_name).first()
        if this_usr1:
            if this_usr1.spon_password==spon_password:
                session['spon_user_name']=spon_user_name
                return render_template("sponsor_dashboard.html")
            else:
                return render_template("index.html")
    return render_template("sponsor_login.html")'''





'''@app.route("/inf_dashboard", methods=['GET'])
def inf_dashboard():
    user_name=session.get("user_name")
    influencer=inf_info.query.filter_by(user_name=user_name).first()

    if not influencer:
        return redirect(url_for("inf_login"))
    
    return render_template("inf_dashboard.html", influencer=influencer)'''


##GOING TO DASHBOARD##
@app.route("/sponsor_dashboard", methods=["GET"])                                          
def sponsor_dashboard():
    user_name = session.get("spon_user_name")
    if not user_name:
        flash("User not logged in", "error")
        return redirect(url_for("sponsor_login"))

    sponsor = spon_info.query.filter_by(spon_user_name=user_name).first()
    if not sponsor:
        flash("Sponsor not found", "error")
        return redirect(url_for("sponsor_login"))

    '''sponsor_details = {
        'full_name': sponsor.spon_full_name,
        'email': sponsor.email,
        'industry': sponsor.industry,
        'evaluation': sponsor.evaluation
    }'''
    
    #return render_template("sponsor_dashboard.html", sponsor_details=sponsor_details)
    return render_template("sponsor_dashboard.html", sponsor=sponsor)


'''
@app.route("/sponsor_dashboard", methods=["GET"])
def sponsor_dashboard():
    user_name=session.get("spon_user_name")
    sponsorjin=spon_info.query.filter_by(spon_user_name=user_name).first()

    if not sponsorjin:
        flash("Sponsor not found", "error")
        return redirect(url_for("sponsor_login"))
    
    
    
    sponsor_details = {'full_name': sponsorjin.spon_full_name,'email': sponsorjin.email,'industry': sponsorjin.industry,'evaluation': sponsorjin.evaluation}
    #return render_template("sponsor_dashboard.html", spon_user_name=sponsorjin.spon_user_name, sponsor_details=sponsor_details)
    return render_template("sponsor_dashboard.html", sponsor_details=sponsor_details)'''
    

##GOING TO CAMPAIGN##
@app.route("/sponsor_campaign", methods=["GET"])
def sponsor_campaign():
    spon_user_name=session.get("spon_user_name")
    if not spon_user_name:
        return render_template("sponsor_login.html")
    
    s2=spon_info.query.filter_by(spon_user_name=spon_user_name).first()
    if not s2:
        return render_template("sponsor_login.html")
    
    campaigns=campaign.query.filter_by(spon_id=s2.spon_id).all()
    return render_template ("sponsor_campaign.html", campaigns=campaigns)


##GOING TO VIEW CAMPAIGN##
@app.route("/view_campaign/<int:camp_id>", methods=['GET'])
def view_campaign(camp_id):
    s3=campaign.query.get(camp_id)
    if not s3:
        return render_template("sponsor_campaign.html")
    return render_template("view_campaign.html", c1=s3)



##GOING TO EDIT CAMPAIGN##
@app.route("/edit_campaign/<int:camp_id>", methods=['GET', 'POST'])
def edit_campaign(camp_id):
    user_name = session.get("spon_user_name")
    sponsor = spon_info.query.filter_by(spon_user_name=user_name).first()
    s4=campaign.query.get(camp_id)
    if not s4:
        return render_template("sponsor_campaign.html")
    if request.method=="POST":
        s4.name=request.form.get("name")
        s4.description=request.form.get("description")
        s4.sdate=datetime.strptime(request.form.get("sdate"), "%Y-%m-%d").date()
        s4.edate=datetime.strptime(request.form.get("edate"), "%Y-%m-%d").date()
        s4.budget=request.form.get("budget")
        s4.goals=request.form.get("goals")
        s4.Visibility=request.form.get("visibility")
        db.session.commit()
        return render_template("sponsor_dashboard.html", sponsor=sponsor)
    return render_template("edit_campaign.html", c2=s4)


##GOING TO DELETE CAMPAIGN##
@app.route("/delete_campaign/<int:camp_id>", methods=['GET'])
def delete_campaign(camp_id):
    user_name = session.get("spon_user_name")
    sponsor = spon_info.query.filter_by(spon_user_name=user_name).first()
    s5=campaign.query.get(camp_id)
    if not s5:
        return render_template("sponsor_campaign.html")
    db.session.delete(s5)
    db.session.commit()
    return render_template("sponsor_dashboard.html", sponsor=sponsor)



##GOING TO FIND##
@app.route("/sponsor_find", methods=['GET', 'POST'])
def sponsor_find():
    categories=["Tech", "Gaming", "Writing and Literature", "Movies", "Fitness", "Food", "Lifestyle", "Pop-Culture", "Finance", "Pet", "Beauty", "Travel", "Performing Arts", "Education", "Other"]
    influencers_query=inf_info.query.filter_by(inf_flag_status="Unflagged")

    if request.method=="POST":
        category=request.form.get('category')
        min_followers=request.form.get('min_followers')
        max_followers=request.form.get('max_followers')

        if category and category!='All':
            influencers_query=influencers_query.filter_by(category=category)

        if min_followers:
            influencers_query=influencers_query.filter(inf_info.no_of_followers >= int(min_followers))

        if max_followers:
            influencers_query=influencers_query.filter(inf_info.no_of_followers <= int(max_followers))

    influencers=influencers_query.all()

    return render_template("sponsor_find.html", categories=categories, influencers=influencers)    
    


##CREATE CAMPAIGN FOR SPONSOR##
@app.route("/sponsor_create_campaign", methods=['GET', 'POST'])
def sponsor_create_campaign():
    if request.method=="POST":
        spon_user_name=session.get("spon_user_name")
        s1=spon_info.query.filter_by(spon_user_name=spon_user_name).first()
        if not s1:
            return render_template("sponsor_dashboard.html")
        
        if s1.spon_flag_status=="Flagged":
            return "YOU ARE FLAGGED AND CANNOT CREATE CAMPAIGNS", 403
        name=request.form.get("name")
        description=request.form.get("description")
        sdate=datetime.strptime(request.form.get("sdate"), "%Y-%m-%d").date()
        edate=datetime.strptime(request.form.get("edate"), "%Y-%m-%d").date()
        budget=request.form.get("budget")
        goals=request.form.get("goals")
        Visibility=request.form.get("visibility")

        new_campaign=campaign(spon_id=s1.spon_id, name=name, description=description, sdate=sdate, edate=edate, budget=budget, goals=goals, Visibility=Visibility )
        db.session.add(new_campaign)
        db.session.commit()
        return render_template("sponsor_create_campaign.html")
        #return render_template("sponsor_dashboard.html")
    return render_template("sponsor_create_campaign.html")


##GOING TO CREATE AD REQUEST##
@app.route("/create_ad_request/<int:camp_id>", methods=['GET', 'POST'])
def create_ad_request(camp_id):
    campaign_data = campaign.query.filter_by(camp_id=camp_id, camp_flag_status="Unflagged").first()
    influencers = inf_info.query.filter_by(inf_flag_status="Unflagged").all()
    
    if not campaign_data:
        
        return "THE CAMPAIGN IS FLAGGED OR DOESN'T EXIST!" 

    if request.method == 'POST':
        message = request.form.get('message')
        requirements = request.form.get('requirements')
        payment = int(request.form.get('payment'))
        inf_id = int(request.form.get('influencer'))
        
        new_ad_request = adreq(camp_id=camp_id,inf_id=inf_id,messeges=message,requirements=requirements,payment=payment,sender="S")
        
        db.session.add(new_ad_request)
        db.session.commit()
        
        return redirect(url_for('sponsor_dashboard')) 
    
    return render_template("create_ad_request.html", campaign=campaign_data, influencers=influencers)

##GOING TO VIEW INFLUENCER##
@app.route("/view_influencer/<int:inf_id>", methods=['GET'])
def view_influencer(inf_id):
    influencer=inf_info.query.get_or_404(inf_id)
    return render_template("view_influencer.html", influencer=influencer)



##GOING TO AD REQUEST##
@app.route("/create_ad_request_2/<int:inf_id>", methods=['GET', 'POST'])
def create_ad_request_2(inf_id):
    influencer=inf_info.query.get_or_404(inf_id)

    spon_user_name = session.get('spon_user_name')
    sponsor = spon_info.query.filter_by(spon_user_name=spon_user_name).first()

    if request.method=="POST":
        camp_id=request.form['camp_id']
        messeges=request.form['messeges']
        requirements=request.form['requirements']
        payment=request.form['payment']

        new_adreq=adreq(camp_id=camp_id, inf_id=inf_id, messeges=messeges, requirements=requirements, payment=payment,sender="S")
        
        db.session.add(new_adreq)
        db.session.commit()
        
        return redirect(url_for('sponsor_dashboard'))
    
    campaigns=campaign.query.filter_by(spon_id=sponsor.spon_id, camp_flag_status="Unflagged").all()
    return render_template("create_ad_request_2.html", influencer=influencer, campaigns=campaigns)



###GOING TO REQUESTS SENT##
@app.route("/sponsor_requests_sent", methods=["GET"])
def sponsor_requests_sent():
    sponsor_user_name = session.get("spon_user_name")
    if not sponsor_user_name:
        return redirect(url_for("sponsor_login"))

    sponsor = spon_info.query.filter_by(spon_user_name=sponsor_user_name).first()
    if not sponsor:
        return redirect(url_for("sponsor_login"))

    ad_requests = db.session.query(adreq, campaign, inf_info).join(campaign, adreq.camp_id == campaign.camp_id).join(inf_info, adreq.inf_id == inf_info.inf_id).filter(campaign.spon_id == sponsor.spon_id, adreq.req_status == "PENDING", adreq.sender=='S').all()

    return render_template("sponsor_requests_sent.html", ad_requests=ad_requests)


'''@app.route("/sponsor_requests_sent", methods=["GET"])
def sponsor_requests_sent():
    sponsor_user_name = session.get("spon_user_name")
    if not sponsor_user_name:
        return redirect(url_for("sponsor_login"))
    sponsor = spon_info.query.filter_by(spon_user_name=sponsor_user_name).first()
    if not sponsor:
        return redirect(url_for("sponsor_login"))
    
    ad_requests = adreq.query.filter_by(sender="S").join(campaign, adreq.camp_id == campaign.camp_id).join(inf_info, adreq.inf_id == inf_info.inf_id).filter(campaign.spon_id == sponsor.spon_id, adreq.req_status == "PENDING").all()
    
    return render_template("sponsor_requests_sent.html", ad_requests=ad_requests)'''



#UPDATE AD REQUESTS##
@app.route("/sponsor_update_ad_request/<int:req_id>", methods=['GET','POST'])
def sponsor_update_ad_request(req_id):
    ad_request=adreq.query.get_or_404(req_id)
    if request.method=="POST":
        ad_request.messeges=request.form.get("message")
        ad_request.requirements=request.form.get("requirements")
        ad_request.payment=request.form.get("payment")

        db.session.commit()
        return redirect(url_for("sponsor_requests_sent"))
    
    return render_template("sponsor_update_ad_request.html", ad_request=ad_request)



##DELETE AD REQUESTS##
@app.route("/sponsor_delete_ad_request/<int:req_id>", methods=['GET'])
def sponsor_delete_ad_request(req_id):
    ad_request=adreq.query.get_or_404(req_id)
    db.session.delete(ad_request)
    db.session.commit()
    return redirect(url_for("sponsor_requests_sent"))


'''##CREATE AD REQUEST FOR SPONSOR##
@app.route("/create_ad_request/<int:spon_id>/<int:camp_id>", methods=['GET','POST'])
def create_ad_request(spon_id, camp_id):
    cmp=campaign.query.get_or_404(camp_id)
    spn=spon_info.query.get_or_404(spon_id)
    influencers=inf_info.query.filter_by(inf_flag_status="Unflagged").all()

    if request.method=="POST":
        message=request.form.get("message")
        requirements_text=request.form.get("requirements")
        payment=int(request.form.get('payment'))
        inf_id=int(request.form.get("influencer"))
        camp_id=int(request.form.get("campaign_id"))

        new_ad_request=adreq(camp_id=camp_id, inf_id=inf_id,messages=message, reqruirements=requirements_text, payment=payment, sender="Sponsor")

        db.session.add(new_ad_request)
        db.session.commit()

        return render_template(f'/sponsor_campaign/{spn.id}/{cmp.id}')
    
    return render_template("create_ad_request.html", cmp=cmp, spn=spn, influencers=influencers)'''


##INFLUENCER AT WORK##
@app.route("/sponsor_workers", methods=['GET'])
def sponsor_workers():
    sponsor_user_name=session.get("spon_user_name")
    if not sponsor_user_name:
        return redirect(url_for("sponsor_login"))
    sponsor=spon_info.query.filter_by(spon_user_name=sponsor_user_name).first()
    if not sponsor:
        return redirect(url_for("sponsor_login"))

    ad_requests=db.session.query(adreq, campaign, inf_info).join(campaign, adreq.camp_id==campaign.camp_id).join(inf_info, adreq.inf_id==inf_info.inf_id).filter(campaign.spon_id==sponsor.spon_id, adreq.req_status=="ACCEPTED").all()
    return render_template("sponsor_workers.html", ad_requests=ad_requests)  



##GOING TO REQUEST STATUS##
@app.route("/sponsor_accepted_or_rejected", methods=['GET'])
def sponsor_accepted_or_rejected():
    sponsor_user_name=session.get("spon_user_name")
    if not sponsor_user_name:
        return redirect(url_for("sponsor_login"))
    
    sponsor=spon_info.query.filter_by(spon_user_name=sponsor_user_name).first()
    if not sponsor:
        return redirect(url_for("sponsor_login"))
    ad_requests=db.session.query(adreq, campaign, inf_info).join(campaign, adreq.camp_id==campaign.camp_id).join(inf_info, adreq.inf_id==inf_info.inf_id).filter(campaign.spon_id==sponsor.spon_id, adreq.sender=="S", adreq.req_status.in_(["ACCEPTED","REJECTED"])).all()
    # ad_requests=adreq.query.join(campaign).filter(campaign.spon_id==sponsor.spon_id, adreq.sender=='S').all()
    return render_template("sponsor_accepted_or_rejected.html", ad_requests=ad_requests)


##GOING TO RECEIVED REQUEST##
@app.route("/sponsor_requests_rec", methods=['GET', 'POST'])
def sponsor_requests_rec():
    user_name = session.get('spon_user_name')
    sponsor = spon_info.query.filter_by(spon_user_name=user_name).first()
    
    if not sponsor:
        return redirect(url_for("sponsor_login"))
    
    ad_requests = adreq.query.join(campaign, adreq.camp_id == campaign.camp_id).filter(adreq.sender == 'I', adreq.req_status == 'PENDING', campaign.spon_id == sponsor.spon_id).all()
    
    if request.method == 'POST':
        req_id = request.form.get('req_id')
        action = request.form.get('action')
        ad_request = adreq.query.get_or_404(req_id)
        
        if action == 'accept':
            ad_request.req_status = 'ACCEPTED'
        elif action == 'reject':
            ad_request.req_status = 'REJECTED'
        elif action == 'negotiate':
            ad_request.req_status = 'NEGOTIATE'
        
        db.session.commit()
        return redirect(url_for('sponsor_requests_rec'))
    
    return render_template("sponsor_requests_rec.html", requests=ad_requests)


'''@app.route("/sponsor_requests_rec", methods=['GET','POST'])
def sponsor_requests_rec():
    user_name=session.get('user_name')
    sponsor=spon_info.query.filter_by(spon_user_name=user_name).first()

    if not sponsor:
        return redirect(url_for("sponsor_login"))
    ad_requests=adreq.query.join(campaign, adreq.cam_id==campaign.camp_id).filter(adreq.sender=="I", adreq.req_status=="PENDING", campaign.spon_id==sponsor.spon_id).all()
    return render_template("sponsor_requests_rec.html", ad_requests=ad_requests)

##ACCEPT,REJECT,NEGOTIATE##
@app.route("/inf_arn/<int:req_id>", methods=['POST'])
def inf_arn(req_id):
    action=request.form.get('action')
    ad_request=adreq.query.get_or_404(req_id)

    if action=="accept":
        ad_request.req_status="ACCEPTED"
    elif action=="reject":
        ad_request.req_status="REJECTED"
    elif action=="negotiate":
        ad_request.req_status="NEGOTIATE"
    
    db.session.commit()
    return redirect(url_for("sponsor_requests_rec"))'''

##SPONSOR PROFILE##
@app.route("/sponsor_prof", methods=['GET','POST'])
def sponsor_prof():
    user_name=session.get("spon_user_name")
    sponsor=spon_info.query.filter_by(spon_user_name=user_name).first()

    if not sponsor:
        flash("Sponsor not found","error")
        return redirect(url_for("sponsor_dashboard"))
    
    if request.method=="POST":
        sponsor.spon_full_name=request.form["spon_full_name"]
        sponsor.spon_user_name=request.form["spon_user_name"]
        sponsor.email=request.form["email"]
        sponsor.industry=request.form["industry"]
        sponsor.evaluation=request.form["evaluation"]

        db.session.commit()
        flash("PROFILE UPDATED SUCCESFULLY","SUCCESS")
        return redirect(url_for("sponsor_prof"))
    
    return render_template("sponsor_prof.html", sponsor=sponsor)
        

##################################I N F L U E N C E R##################################

##INFLUENCER DASHBOARD##
@app.route("/inf_dashboard", methods=['GET'])
def inf_dashboard():
    user_name=session.get("user_name")
    influencer=inf_info.query.filter_by(user_name=user_name).first()

    if not influencer:
        return redirect(url_for("inf_login"))
    
    return render_template("inf_dashboard.html", influencer=influencer)



##INFLUENCER REGISTRATION##
@app.route("/inf_registration", methods=['GET','POST'])
def inf_registration():
    if request.method=="POST":
        email=request.form.get("email")
        full_name=request.form.get("name")
        user_name=request.form.get("uname")
        category=request.form.get("category")
        niche=request.form.get("niche")
        no_of_followers=request.form.get("followers")
        password=request.form.get("password")
        usr=inf_info.query.filter_by(user_name=user_name).first()
        if not usr:
            new_user=inf_info(email=email,full_name=full_name,user_name=user_name,category=category,niche=niche,no_of_followers=no_of_followers,password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template("inf_login.html")
        else:
            return render_template("index.html")
    return render_template("inf_registration.html")



'''##INFLUENCER LOGIN##
@app.route("/inf_login", methods=['GET','POST'])
def inf_login():
    if request.method=="POST":
        user_name=request.form.get("uname")
        password=request.form.get("password")
        this_usr=inf_info.query.filter_by(user_name=user_name).first()
        if this_usr:
            if this_usr.password==password:
                session['user_name']=user_name
                return render_template("inf_dashboard.html")
            else:
                return render_template("index.html")
    return render_template("inf_login.html")'''

# Route for influencer login
@app.route("/inf_login", methods=['GET','POST'])
def inf_login():
    if request.method == "POST":
        user_name = request.form.get("uname")
        password = request.form.get("password")
        
       
        influencer = inf_info.query.filter_by(user_name=user_name, password=password).first()
        
        if influencer:
            
            session['user_name'] = user_name
            
            return redirect(url_for("inf_dashboard"))
        else:
            return render_template("index.html")  
    return render_template("inf_login.html")



##GOING TO FIND##
@app.route("/inf_find", methods=["GET"])
def inf_find():
    sponsor_industry=request.args.get("sponsor_industry")
    budget_min=request.args.get("budget_min")
    budget_max=request.args.get("budget_max")
    start_date_earliest=request.args.get("start_date_earliest")
    start_date_latest=request.args.get("start_date_latest")

    query=db.session.query(campaign, spon_info).join(spon_info, campaign.spon_id == spon_info.spon_id).filter(campaign.camp_flag_status == "Unflagged", campaign.edate >= datetime.now().date(), campaign.Visibility=="Public")

    if sponsor_industry:
        query=query.filter(spon_info.industry.ilike(f"%{sponsor_industry}%"))

    if budget_min:
        query=query.filter(campaign.budget >= int(budget_min))

    if budget_max:
        query=query.filter(campaign.budget <= int(budget_max))

    if start_date_earliest:
        query=query.filter(campaign.sdate >= datetime.strptime(start_date_earliest, "%Y-%m-%d").date())

    if start_date_latest:
        query=query.filter(campaign.sdate <= datetime.strptime(start_date_latest, "%Y-%m%d").date())

    results=query.all()
    c3=[]
    for result in results:
        c4, s5 = result
        c3.append({'camp_id':c4.camp_id, 'name' : c4.name, 'description': c4.description, 'sdate': c4.sdate, 'edate': c4.edate, 'budget': c4.budget, 'Visibility': c4.Visibility, 'goals':c4.goals, 'sponsor_name': s5.spon_full_name})

    return render_template("inf_find.html", c3=c3)



##GOING TO VIEW##
@app.route("/inf_view_campaign/<int:camp_id>")
def inf_view_campaign(camp_id):
    c5=campaign.query.get_or_404(camp_id)
    s6=spon_info.query.get(c5.spon_id)

    return render_template("inf_view_campaign.html", c5=c5, s6=s6)



##GOING TO STATISTICS##
@app.route("/inf_stats", methods=["GET"])
def inf_stats():
    unflagged_sponsors_count=spon_info.query.filter_by(spon_flag_status="Unflagged").count()
    unflagged_campaigns_count=campaign.query.filter_by(camp_flag_status="Unflagged").count()

    active_campaigns_count=campaign.query.filter(campaign.camp_flag_status=="Unflagged", campaign.edate >= datetime.now().date()).count()

    sponsors_by_industry=db.session.query(spon_info.industry, db.func.count(spon_info.spon_id)).filter_by(spon_flag_status="Unflagged").group_by(spon_info.industry).all()

    average_budget=db.session.query(db.func.avg(campaign.budget)).filter_by(camp_flag_status="Unflagged").scalar()

    campaigns_by_visibility=db.session.query(campaign.Visibility, db.func.count(campaign.camp_id)).filter_by(camp_flag_status="Unflagged").group_by(campaign.Visibility).all()

    top_industries=db.session.query(spon_info.industry, db.func.count(spon_info.spon_id)).filter_by(spon_flag_status="Unflagged").group_by(spon_info.industry).order_by(db.func.count(spon_info.spon_id).desc()).limit(3).all()

    average_evaluation=db.session.query(db.func.avg(spon_info.evaluation)).filter_by(spon_flag_status="Unflagged").scalar()

    return render_template("inf_stats.html", unflagged_sponsors_count=unflagged_sponsors_count,unflagged_campaigns_count=unflagged_campaigns_count,active_campaigns_count=active_campaigns_count, sponsors_by_industry=sponsors_by_industry,average_budget=average_budget,campaigns_by_visibility=campaigns_by_visibility, top_industries=top_industries,average_evaluation=average_evaluation)


##RECEIVED REQUEST##
@app.route("/inf_rec", methods=['GET', 'POST'])
def inf_rec():
    user_name = session.get('user_name')
    influencer = inf_info.query.filter_by(user_name=user_name).first()
    
    if not influencer:
        return redirect(url_for("inf_login"))
    
    ad_requests = adreq.query.filter_by(inf_id=influencer.inf_id, req_status="PENDING", sender="S").all()
    
    if request.method == "POST":
        req_id = int(request.form.get("req_id"))
        action = request.form.get('action')

        ad_request = adreq.query.get_or_404(req_id)
        
        if action == "accept":
            ad_request.req_status = "ACCEPTED"
        elif action == "reject":
            ad_request.req_status = "REJECTED"
        elif action == "negotiate":
            ad_request.req_status = "NEGOTIATION"
        
        ad_request.sender = "S"
        db.session.commit()

        return redirect(url_for("inf_rec"))
    
    return render_template("inf_rec.html", requests=ad_requests)

##ACCEPT,REJECT,NEGOTIATE##
@app.route("/handle_action/<action>/<int:req_id>", methods=['GET', 'POST'])
def handle_action(action, req_id):
    user_name = session.get('user_name')
    influencer = inf_info.query.filter_by(user_name=user_name).first()
    
    if not influencer:
        return redirect(url_for("inf_login"))

    ad_request = adreq.query.get_or_404(req_id)
    
    if not ad_request or ad_request.inf_id != influencer.inf_id:
        return redirect(url_for("inf_rec"))
    
    if action == "accept":
        ad_request.req_status = "ACCEPTED"
    elif action == "reject":
        ad_request.req_status = "REJECTED"
    elif action == "negotiate":
        ad_request.req_status = "NEGOTIATION"

    ad_request.sender = "S"
    db.session.commit()

    return redirect(url_for("inf_rec"))
'''##ACCEPTING OR REJECTING REQ##
@app.route("/inf_rec", methods=['GET', 'POST'])
def inf_rec():
    user_name=session.get('user_name')
    influencer=inf_info.query.filter_by(user_name=user_name).first()
    if not influencer:
        return redirect("inf_stats.html")
    
    requests=adreq.query.filter_by(inf_id=influencer.inf_id, req_status="PENDING").all()

    if request.method=="POST":
        req_id=int(request.form.get("req_id"))
        action=request.form.get('action')

        ad_request=adreq.query.get_or_404(req_id)
        if action=="accepted":
            ad_request.req_status="Accepted"
        elif action=="reject":
            ad_request.req_status="Rejected"
        elif action=="negotiate":
            ad_request.req_status="Negotiation"
        
        ad_request.sender="Sponsor"

        db.session.commit()

        return redirect("inf_rec.html")
    
    return render_template("inf_rec.html", requests=requests)'''

'''##RECEIVED REQUESTS##
@app.route("/inf_rec")
def inf_rec():
    if 'user_name' in session:
        user_name = session['user_name']
        influencer = inf_info.query.filter_by(user_name=user_name).first()
        
        if influencer:
            ad_requests = adreq.query.join(campaign).filter(adreq.inf_id == influencer.inf_id, adreq.req_status=="PENDING").all()
            return render_template("inf_rec.html", influencer=influencer, ad_requests=ad_requests)
    
    return redirect(url_for("inf_login"))'''


'''##ACCEPTANCE OR REJECTION RESPONSE##
@app.route("/handle_action/<action>/<int:req_id>", methods=['GET', 'POST'])
def handle_action(action, req_id):
    if 'user_name' in session:
        user_name=session['user_name']
        influencer=inf_info.query.filter_by(user_name=user_name).first()
        if influencer:
            ad_request=adreq.query.get(req_id)

            if not ad_request or ad_request.inf_id!=influencer.inf_id:
                return redirect(url_for("inf_rec"))
            
            if action=="accept":
                ad_request.req_status="ACCEPTED"
            elif action=="rejec":
                ad_request.req_status="REJECTED"

            db.session.commit()

            return redirect(url_for("inf_rec"))
    return redirect(url_for("inf_dashboard"))'''



'''@app.route("/inf_camp")
def inf_camp():
    if 'user_name' in session:
        user_name = session['user_name']
        influencer = inf_info.query.filter_by(user_name=user_name).first()

        if influencer:
            # Fetch campaigns where ad request status is "ACCEPTED" for the influencer
            campaigns = campaign.query.join(adreq).filter(adreq.inf_id == influencer.inf_id, adreq.req_status == "ACCEPTED").all()

            return render_template("inf_camp.html", influencer=influencer, campaigns=campaigns)
    
    return redirect(url_for("inf_dashboard"))'''



'''@app.route("/inf_rec", methods=['GET', 'POST'])
def inf_rec():
    inf_id = session.get('inf_id')
    if not inf_id:
        return redirect(url_for('inf_dashboard'))  # Redirect to login if influencer not logged in
    
    influencer = inf_info.query.get(inf_id)
    if not influencer:
        return "Influencer not found", 404
    
    if request.method == 'POST':
        req_id = request.form.get('req_id')
        action = request.form.get('action')
        
        ad_request = adreq.query.get(req_id)
        if ad_request and ad_request.inf_id == inf_id:
            if action == 'accept':
                ad_request.req_status = 'ACCEPT'
            elif action == 'reject':
                ad_request.req_status = 'REJECT'
            elif action == 'negotiate':
                return redirect(url_for("inf_find"))  # Implement negotiation logic
            
            db.session.commit()
    
    adrequests_rec = adreq.query.filter_by(inf_id=inf_id, sender="S", req_status="PENDING").all()
    
    return render_template("inf_rec.html", influencer=influencer, adrequests_rec=adrequests_rec)'''




'''@app.route("/inf_rec", methods=['GET','POST'])
def inf_rec():
    influencer_user_name=session.get("inf_user_name")
    if not influencer_user_name:
        return redirect(url_for("inf_dashboard"))
    influencer=inf_info.query.filter_by(user_name=influencer_user_name).first()
    if not influencer:
        return redirect(url_for("inf_dashboard"))
    
    if request.method=="POST":
        req_id=request.form.get("req_id")
        action=request.form.get("action")
        ad_request=adreq.query.get_or_404(req_id)

        if action=="accepted":
            ad_request.req_status="ACCEPT"
        elif action=="reject":
            ad_request.req_status="REJECTED"
        elif action=="negotiate":
            ad_request.req_status="NEGOTIATE"

        db.session.commit()
        return redirect(url_for("inf_rec"))
    
    ad_requests=db.session.query(adreq, campaign, spon_info).join(campaign, adreq.camp_id==campaign.camp_id).join(spon_info, campaign.spon_id==spon_info.spon_id).filter(adreq.inf_id==influencer.inf_id, adreq.req_status=="PENDING", adreq.sender=="S").all()
    
    return render_template("inf_rec.html", ad_requests=ad_requests)'''


'''
##REQUEST STATUS PAGE##
@app.route("/sponsor_accepted_or_rejected", methods=['GET'])
def sponsor_accepted_or_rejected():
    sponsor_user_name=session.get("spon_user_name")
    if not sponsor_user_name:
        return redirect(url_for("sponsor_login"))
    sponsor=spon_info.query.filter_by(spon_user_name=sponsor_user_name).first()
    if not sponsor:
        return redirect(url_for("sponsor_login"))
    
    ad_requests=db.session.query(adreq, campaign, inf_info).join(campaign, adreq.camp_id==campaign.camp_id).join(inf_info, adreq.inf_id==inf_info.inf_id).filter(campaign.spon_id==sponsor.spon_id, adreq.req_status!="PENDING").all()

    return render_template("sponsor_accepted_or_rejected.html", ad_requests=ad_requests)'''

##GOING TO REQUEST##
@app.route("/inf_request_campaign/<int:camp_id>", methods=['GET','POST'])
def inf_request_campaign(camp_id):
    user_name=session.get("user_name")
    influencer=inf_info.query.filter_by(user_name=user_name).first()

    if not influencer:
        return redirect(url_for("inf_login"))
    
    campaign_data=campaign.query.get_or_404(camp_id)

    if request.method=="POST":
        messages=request.form.get('messages')
        requirements=request.form.get('requirements')
        payment=request.form.get('payment')

        new_ad_request=adreq(camp_id=camp_id, inf_id=influencer.inf_id, messeges=messages, requirements=requirements, payment=payment, sender="I")

        db.session.add(new_ad_request)
        db.session.commit()
        return redirect(url_for("inf_find"))
    
    return render_template("inf_request_campaign.html", influencer=influencer, campaign=campaign_data)


##GOING TO SENT REQUESTS##
@app.route("/inf_sent", methods=["GET"])
def inf_sent():
    user_name = session.get("user_name")
    if not user_name:
        return redirect(url_for("inf_login"))

    influencer = inf_info.query.filter_by(user_name=user_name).first()
    if not influencer:
        return redirect(url_for("inf_login"))

    ad_requests = db.session.query(adreq, campaign, spon_info).join(campaign, adreq.camp_id == campaign.camp_id).join(spon_info, campaign.spon_id == spon_info.spon_id).filter(adreq.inf_id==influencer.inf_id, adreq.sender=="I", adreq.req_status=="PENDING").all()

    return render_template("inf_sent.html", ad_requests=ad_requests)


'''@app.route("/inf_sent", methods=['GET'])
def inf_sent():
    user_name=session.get('user_name')
    influencer=inf_info.query.filter_by(user_name=user_name).first()

    if not influencer:
        return redirect(url_for("inf_login"))
    
    ad_requests = db.session.query(adreq, campaign, spon_info).join(campaign, adreq.camp_id == campaign.camp_id).join(spon_info, campaign.spon_id == spon_info.spon_id).filter(adreq.inf_id == influencer.inf_id, adreq.sender == "I", adreq.req_status == "PENDING").all()
    return render_template("inf_sent.html", ad_requests=ad_requests)'''

##GOING TO UPDATE AD REQUEST##
@app.route("/inf_update_ad_request/<int:req_id>", methods=['GET','POST'])
def inf_update_ad_request(req_id):
    ad_request=adreq.query.get_or_404(req_id)
    if request.method=="POST":
        ad_request.messeges=request.form['message']
        ad_request.requirements=request.form['requirements']
        ad_request.payment=request.form['payment']
        db.session.commit()
        return redirect(url_for("inf_sent"))
    return render_template("inf_update_ad_request.html", ad_request=ad_request)

##GOING TO DELETE AD REQUEST##
@app.route("/inf_delete_ad_request/<int:req_id>", methods=['GET','POST'])
def inf_delete_ad_request(req_id):
    ad_request=adreq.query.get_or_404(req_id)
    db.session.delete(ad_request)
    db.session.commit()

    return redirect(url_for("inf_sent"))


##GOING TO REQUEST STATUS##
@app.route("/inf_accepted_or_rejected")
def inf_accepted_or_rejected():
    user_name=session.get("user_name")
    influencer=inf_info.query.filter_by(user_name=user_name).first()
    if not influencer:
        return redirect(url_for("inf_login"))
    requests=adreq.query.filter_by(inf_id=influencer.inf_id, sender="I").filter(adreq.req_status.in_(['ACCEPTED','REJECTED'])).all()
    return render_template("inf_accepted_or_rejected.html", requests=requests)


##GOING TO MY CAMPAIGNS##
@app.route("/inf_camp", methods=['GET'])
def inf_camp():
    user_name=session.get('user_name')
    influencer=inf_info.query.filter_by(user_name=user_name).first()
    if not influencer:
        return redirect(url_for("inf_login"))
    accepted_requests=db.session.query(adreq, campaign, spon_info).filter(adreq.inf_id==influencer.inf_id, adreq.req_status=="ACCEPTED", spon_info.spon_flag_status=="Unflagged", adreq.camp_id==campaign.camp_id, campaign.spon_id==spon_info.spon_id).all()
    return render_template("inf_camp.html", campaigns=accepted_requests)


##GOING TO INFLUENCER PROFILE##
@app.route("/inf_prof", methods=['GET','POST'])
def inf_prof():
    user_name=session.get("user_name")
    influencer=inf_info.query.filter_by(user_name=user_name).first()

    if not influencer:
        flash("Influencer not found.", "error")
        return redirect(url_for("inf_login"))
    
    categories = ["Tech", "Gaming", "Writing and Literature", "Movies", "Fitness", "Food", "Lifestyle", "Pop-Culture", "Finance", "Pet", "Beauty", "Travel", "Performing Arts", "Education", "Other"]
    
    if request.method=="POST":
        influencer.email=request.form["email"]
        influencer.full_name=request.form["full_name"]
        influencer.user_name=request.form["user_name"]
        influencer.category=request.form["category"]
        influencer.niche=request.form["niche"]
        influencer.no_of_followers=request.form["no_of_followers"]

        db.session.commit()
        flash("PROFILE UPDATED SUCCESSFULLY", "success")
        return redirect(url_for("inf_prof"))
    
    return render_template("inf_prof.html",influencer=influencer, categories=categories)


##################################A D M I N##################################

##ADMIN DASHBOARD##
@app.route("/admin_dashboard", methods=['GET','POST'])
def admin_dashboard():
    return render_template("admin_dashboard.html")



##ADMIN LOGIN##
@app.route("/admin_login", methods=['GET','POST'])
def admin_login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        if email=="satyaki452@gmail.com" and password=="150894sg": #CONTANTS, HARDCODED FOR ME (ADMIN)
            return render_template("admin_dashboard.html")
    return render_template("admin_login.html")

##PROGRESS##
@app.route("/admin_prog", methods=['GET'])
def admin_prog():
    campaigns=campaign.query.all()
    progress_data=[]
    for camp in campaigns:
        td=(camp.edate-camp.sdate).days
        dp=(datetime.now(timezone.utc).date()-camp.sdate).days
        progress_percentage=min(100, max(0, int((dp/td)*100)))
        progress_data.append((camp, progress_percentage))

    return render_template("admin_prog.html", progress_data=progress_data)


##GOING TO SPONSORS##
@app.route("/admin_spon", methods=['GET', 'POST'])
def admin_spon():
    if request.method == 'POST':
        spon_id = request.form.get("spon_id")
        action = request.form.get("action")
        
        sponsor = spon_info.query.get_or_404(spon_id)
        
        if action == 'flag':
            sponsor.spon_flag_status = "Flagged"
        elif action == 'unflag':
            sponsor.spon_flag_status = "Unflagged"
        
        db.session.commit()
        return redirect(url_for("admin_spon"))
    
    sponsors = spon_info.query.all()
    return render_template("admin_spon.html", sponsors=sponsors)


##GOING TO CAMPAIGNS##
@app.route("/admin_camp", methods=['GET', 'POST'])
def admin_camp():
    if request.method == 'POST':
        camp_id = request.form.get('camp_id')
        action = request.form.get('action')
        
        if camp_id:
            campaign_1 = campaign.query.get_or_404(camp_id)
        
            if action == 'flag':
                campaign_1.camp_flag_status="Flagged"
            elif action == 'unflag':
                campaign_1.camp_flag_status="Unflagged"
            elif action == 'complete':
                campaign_1.completion_status="Completed"
            elif action=='active':
                campaign_1.completion_status="Active"
        
            db.session.commit()
        return redirect(url_for('admin_camp'))
    
    campaigns = campaign.query.all()
    return render_template("admin_camp.html", campaigns=campaigns)


##GOING TO INFLUENCERS##
@app.route("/admin_inf", methods=['GET','POST'])
def admin_inf():
    if request.method=='POST':
        inf_id=request.form.get('inf_id')
        action=request.form.get('action')

        if inf_id:
            influencer=inf_info.query.get_or_404(inf_id)
            if action=="flag":
                influencer.inf_flag_status="Flagged"
            elif action=="unflag":
                influencer.inf_flag_status="Unflagged"
            db.session.commit()

        return redirect(url_for('admin_inf'))
    
    influencers=inf_info.query.all()
    return render_template("admin_inf.html", influencers=influencers)



##GOING TO AD REQUESTS##
@app.route("/admin_req", methods=['GET'])
def admin_req():
    ad_requests=adreq.query.all()
    return render_template("admin_req.html", ad_requests=ad_requests)


##GOING TO INFLUENCER STATS##
@app.route("/admin_inf_stats", methods=['GET'])
def admin_inf_stats():
    influencers=inf_info.query.all()
    ad_requests=adreq.query.all()

    names=[inf.full_name for inf in influencers]
    followers=[inf.no_of_followers for inf in influencers]
    categories=[inf.category for inf in influencers]

    payments = [req.payment for req in ad_requests]
    
    
    total_influencers = len(influencers)
    avg_followers = sum(followers) / total_influencers if total_influencers > 0 else 0
    category_counts = {category: categories.count(category) for category in set(categories)}
    
    highest_followers = max(followers) if followers else 0
    lowest_followers = min(followers) if followers else 0
    highest_payment = max(payments) if payments else 0
    lowest_payment = min(payments) if payments else 0
    avg_payment = sum(payments) / len(payments) if payments else 0

    data = {'names': names,'followers': followers,'categories': categories,'total_influencers': total_influencers,'avg_followers': avg_followers,'category_counts': category_counts,'highest_followers': highest_followers,'lowest_followers': lowest_followers,'highest_payment': highest_payment,'lowest_payment': lowest_payment,'avg_payment': avg_payment}

    return render_template("admin_inf_stats.html", data=data)


##GOING TO SPONSOR STATS##
@app.route("/admin_spon_stats", methods=['GET'])
def admin_spon_stats():
    sponsors = spon_info.query.all()
    total_sponsors = len(sponsors)
    avg_evaluation = sum([s.evaluation for s in sponsors]) / total_sponsors if total_sponsors > 0 else 0
    highest_evaluation = max([s.evaluation for s in sponsors], default=0)
    lowest_evaluation = min([s.evaluation for s in sponsors], default=0)
    highest_budget = max([c.budget for s in sponsors for c in s.campaigns], default=0)
    lowest_budget = min([c.budget for s in sponsors for c in s.campaigns], default=0)
    avg_budget = sum([c.budget for s in sponsors for c in s.campaigns]) / (len([c.budget for s in sponsors for c in s.campaigns]) or 1)
    industry_counts = {industry: sum([1 for s in sponsors if s.industry == industry]) for industry in set(s.industry for s in sponsors)}
    
    ad_requests = adreq.query.all()
    total_ad_requests = len(ad_requests)
    accepted_ad_requests = sum(1 for r in ad_requests if r.req_status == "ACCEPTED")
    rejected_ad_requests = sum(1 for r in ad_requests if r.req_status == "REJECTED")
    ad_requests_by_sponsors = sum(1 for r in ad_requests if r.sender == "S")
    ad_requests_by_influencers = sum(1 for r in ad_requests if r.sender == "I")

    data = {"total_sponsors": total_sponsors,"avg_evaluation": avg_evaluation,"highest_evaluation": highest_evaluation,"lowest_evaluation": lowest_evaluation,"highest_budget": highest_budget,"lowest_budget": lowest_budget,"avg_budget": avg_budget,"industry_counts": industry_counts,"total_ad_requests": total_ad_requests,"accepted_ad_requests": accepted_ad_requests,"rejected_ad_requests": rejected_ad_requests,"ad_requests_by_sponsors": ad_requests_by_sponsors,"ad_requests_by_influencers": ad_requests_by_influencers,"names": [s.spon_full_name for s in sponsors],"budgets": [sum([c.budget for c in s.campaigns]) for s in sponsors]}
    return render_template("admin_spon_stats.html", data=data)


##GOING TO FIND INFLUENCER##
@app.route("/admin_find_inf",methods=['GET'])
def admin_find_inf():
    category=request.args.get('category')
    min_followers=request.args.get("min_followers", type=int)
    max_followers=request.args.get("max_followers", type=int)

    query=inf_info.query
    
    if category:
        query=query.filter_by(category=category)
    if min_followers is not None:
        query=query.filter(inf_info.no_of_followers>=min_followers)
    if max_followers is not None:
        query=query.filter(inf_info.no_of_followers<=max_followers)

    influencers=query.all()

    return render_template("admin_find_inf.html", influencers=influencers)



##GOING TO FIND SPONSOR##
@app.route("/admin_find_spon", methods=['GET'])
def admin_find_spon():
    industry=request.args.get("industry")
    min_evaluation=request.args.get("min_evaluation", type=int)
    max_evaluation=request.args.get("max_evaluation", type=int )

    query=spon_info.query

    if industry:
        query=query.filter_by(industry=industry)
    if min_evaluation is not None:
        query=query.filter(spon_info.evaluation>=min_evaluation)
    if max_evaluation is not None:
        query=query.fiter(spon_info.evaluation<=max_evaluation)

    sponsors=query.all()

    return render_template("admin_find_spon.html", sponsors=sponsors)
