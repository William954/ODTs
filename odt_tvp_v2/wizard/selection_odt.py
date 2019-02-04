from odoo import api, _, tools, fields, models, exceptions
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time    


class OdtSelection(models.TransientModel):
    _name = 'crm.odt.wizard1'
    _description = 'Wizad para la seleccion de ODT a crear'

    areas = fields.Selection([('1','BTL/PDV'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),
                             ('6','Marketing Digital'),('7','Medios'),('8','Logistica'),('9','Estrategia')],
                              string='Area',requiered=True, track_visibility=True)

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity')

    def create_odt(self,vals):
        self.ensure_one()

        if self.areas == '1':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_btl').id
            form_view_id = self.env.ref('odt_tvp_v2.form_btlpdv_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt BTL/PDV'),
                'res_model': 'odt.btlpdv',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id','=', self.opportunity_id)],

            }
            return action

        if self.areas == '2':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_produccion').id
            form_view_id = self.env.ref('odt_tvp_v2.form_produccion_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Produccion'),
                'res_model': 'odt.produccion',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action


        if self.areas == '3':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_diseno').id
            form_view_id = self.env.ref('odt_tvp_v2.form_diseno_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Diseño'),
                'res_model': 'odt.diseno',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action

        if self.areas == '4':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_gestoria').id
            form_view_id = self.env.ref('odt_tvp_v2.form_gestoria_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Gestoria'),
                'res_model': 'odt.gestoria',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action

        if self.areas == '5':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_contact').id
            form_view_id = self.env.ref('odt_tvp_v2.form_contactcenter_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Contact Center'),
                'res_model': 'odt.contactcenter',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action

        if self.areas == '6':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_digital').id
            form_view_id = self.env.ref('odt_tvp_v2.form_digital_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Digital'),
                'res_model': 'odt.digital',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action

        if self.areas == '7':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_medios').id
            form_view_id = self.env.ref('odt_tvp_v2.form_medios_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Medios'),
                'res_model': 'odt.medios',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action


        if self.areas == '9':
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_estrategia').id
            form_view_id = self.env.ref('odt_tvp_v2.form_estrategia_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Estrategia'),
                'res_model': 'odt.estrategia',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action


        if self.areas == '8':            
            kanban_view_id = self.env.ref('odt_tvp_v2.kanban_logistica').id
            form_view_id = self.env.ref('odt_tvp_v2.form_logistica_odt').id

            action = {
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form'),(kanban_view_id, 'kanban')],
                'view_mode': 'form,kanban',
                'name': _('Odt Logistica'),
                'res_model': 'odt.logistica',
                'target': 'new',
                'context':{'default_crm_odt_id': self.opportunity_id.id},
                'domain':  [('crm_odt_id', '=',  self.opportunity_id)],
            }
            return action
