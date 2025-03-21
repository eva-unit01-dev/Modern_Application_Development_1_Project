from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy() #INSTANCE OF SQLALCHEMY

##############TABLE FOR INFLUENCER INFO##############

class inf_info(db.Model):
    __tablename__="inf_info"
    inf_id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String, nullable=False)
    full_name=db.Column(db.String, nullable=False)
    user_name=db.Column(db.String, unique=True, nullable=False)
    category=db.Column(db.String, nullable=False)
    niche=db.Column(db.String, nullable=False)
    no_of_followers=db.Column(db.Integer, nullable=False)
    #email=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    inf_flag_status=db.Column(db.String, default="Unflagged")

    adrequests=db.relationship('adreq', backref='influencer', lazy=True)

##############TABLE FOR SPONSOR INFO##############

class spon_info(db.Model):
    __tablename__="spon_info"
    spon_id=db.Column(db.Integer, primary_key=True)
    spon_type=db.Column(db.String, nullable=False)
    email=db.Column(db.String, nullable=False)
    spon_full_name=db.Column(db.String, nullable=False)
    spon_user_name=db.Column(db.String, unique=True, nullable=False)
    industry=db.Column(db.String, nullable=False)
    evaluation=db.Column(db.Integer, nullable=False)
    spon_password=db.Column(db.String, nullable=False)
    spon_flag_status=db.Column(db.String, default="Unflagged")
    
    campaigns=db.relationship('campaign', backref='sponsor', lazy=True)

##############TABLE FOR CAMPAIGN INFO##############

class campaign(db.Model):
    __tablename__="campaign"
    camp_id=db.Column(db.Integer, primary_key=True)
    spon_id=db.Column(db.Integer, db.ForeignKey("spon_info.spon_id"), nullable=False)
    name=db.Column(db.String, nullable=False)
    description=db.Column(db.Text, nullable=False)
    sdate=db.Column(db.Date, nullable=False)
    edate=db.Column(db.Date, nullable=False)
    budget=db.Column(db.Integer, nullable=False)
    Visibility=db.Column(db.String, nullable=False)
    goals=db.Column(db.Text, nullable=False)
    completion_status=db.Column(db.String, default="Active")
    camp_flag_status=db.Column(db.String, default="Unflagged")

    ad_requests=db.relationship('adreq', backref='campaign', cascade="all, delete-orphan", lazy=True)


##############TABLE FOR AD-REQUEST INFO##############

class adreq(db.Model):
    __tablename__="adreq"
    req_id=db.Column(db.Integer, primary_key=True)
    camp_id=db.Column(db.Integer, db.ForeignKey("campaign.camp_id"), nullable=False)
    inf_id=db.Column(db.Integer, db.ForeignKey("inf_info.inf_id"), nullable=False)
    messeges=db.Column(db.Text, default="DEFAULT TEMPLATE")
    requirements=db.Column(db.Text, nullable=False)
    payment=db.Column(db.Integer, nullable=False)
    req_status=db.Column(db.String, default="PENDING")
    sender=db.Column(db.String, default="WAIT")

    